from datetime import datetime, timedelta, timezone
import hashlib
import secrets
import uuid

import pyotp
from sqlalchemy.orm import Session

from application.auth.schemas import RegisterRequest
from infrastructure.audit.logger import log_event
from infrastructure.email.smtp_client import send_email
from infrastructure.persistence import models
from infrastructure.security.jwt_service import create_access_token, create_refresh_token, decode_token
from infrastructure.security.passwords import hash_password, verify_password
from infrastructure.config import settings


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def register_user(db: Session, request: RegisterRequest, ip_address: str | None, user_agent: str | None):
    existing = db.query(models.User).filter(models.User.email == request.email.lower()).first()
    if existing:
        raise ValueError("Email already registered")

    user = models.User(
        email=request.email.lower(),
        password_hash=hash_password(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    verification = models.EmailVerificationToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(verification)
    db.commit()

    verify_link = f"{settings.app_base_url}/verify-email?token={token}"
    send_email(
        to_email=user.email,
        subject="Verify your MachWork account",
        body=f"Click to verify your account: {verify_link}",
    )

    log_event(
        db=db,
        action="auth.register",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=None,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={"email": user.email},
    )
    return user


def verify_email(db: Session, token: str, ip_address: str | None, user_agent: str | None) -> None:
    token_hash = _hash_token(token)
    record = (
        db.query(models.EmailVerificationToken)
        .filter(models.EmailVerificationToken.token_hash == token_hash, models.EmailVerificationToken.used_at.is_(None))
        .first()
    )
    if not record or record.expires_at < datetime.now(timezone.utc):
        raise ValueError("Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not user:
        raise ValueError("User not found")

    user.email_verified_at = datetime.now(timezone.utc)
    record.used_at = datetime.now(timezone.utc)
    db.commit()

    log_event(
        db=db,
        action="auth.email_verified",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=None,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={"email": user.email},
    )


def login_user(db: Session, email: str, password: str, mfa_code: str | None, ip_address: str | None, user_agent: str | None):
    user = db.query(models.User).filter(models.User.email == email.lower(), models.User.is_active.is_(True)).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    if not user.email_verified_at:
        raise ValueError("Email not verified")

    if user.mfa_enabled:
        if not mfa_code:
            raise ValueError("MFA code required")
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(mfa_code, valid_window=1):
            if not _validate_backup_code(db, user, mfa_code):
                raise ValueError("Invalid MFA code")

    access_token = create_access_token(str(user.id), role=_resolve_primary_role(db, user), company_id=_resolve_primary_company(db, user))
    refresh_token, refresh_token_id, _ = _issue_refresh_token(db, user)

    log_event(
        db=db,
        action="auth.login",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={"refresh_token_id": refresh_token_id},
    )
    return access_token, refresh_token


def _issue_refresh_token(db: Session, user: models.User):
    token_id = str(uuid.uuid4())
    raw_token = create_refresh_token(str(user.id), token_id)
    token_hash = _hash_token(raw_token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_ttl_days)
    record = models.RefreshToken(user_id=user.id, jti=token_id, token_hash=token_hash, expires_at=expires_at)
    db.add(record)
    db.commit()
    db.refresh(record)
    return raw_token, token_id, str(record.id)


def refresh_session(db: Session, refresh_token: str, ip_address: str | None, user_agent: str | None):
    payload = decode_token(refresh_token)
    token_id = payload.get("jti")
    token_hash = _hash_token(refresh_token)
    record = (
        db.query(models.RefreshToken)
        .filter(models.RefreshToken.token_hash == token_hash, models.RefreshToken.revoked_at.is_(None))
        .first()
    )
    if not record or record.expires_at < datetime.now(timezone.utc):
        raise ValueError("Invalid refresh token")
    if token_id and record.jti != token_id:
        raise ValueError("Refresh token mismatch")

    record.revoked_at = datetime.now(timezone.utc)
    db.commit()

    user = db.query(models.User).filter(models.User.id == payload["sub"]).first()
    if not user:
        raise ValueError("User not found")

    access_token = create_access_token(str(user.id), role=_resolve_primary_role(db, user), company_id=_resolve_primary_company(db, user))
    new_refresh_token, new_token_id, new_record_id = _issue_refresh_token(db, user)
    record.replaced_by = uuid.UUID(new_record_id)
    db.commit()

    log_event(
        db=db,
        action="auth.refresh",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={"refresh_token_id": new_token_id, "replaced_by": new_record_id},
    )
    return access_token, new_refresh_token


def initiate_password_reset(db: Session, email: str, ip_address: str | None, user_agent: str | None):
    user = db.query(models.User).filter(models.User.email == email.lower()).first()
    if not user:
        return

    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=2)
    record = models.PasswordResetToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
    db.add(record)
    db.commit()

    reset_link = f"{settings.app_base_url}/reset-password?token={token}"
    send_email(
        to_email=user.email,
        subject="Reset your MachWork password",
        body=f"Reset your password here: {reset_link}",
    )

    log_event(
        db=db,
        action="auth.password_reset_requested",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={},
    )


def reset_password(db: Session, token: str, new_password: str, ip_address: str | None, user_agent: str | None):
    token_hash = _hash_token(token)
    record = (
        db.query(models.PasswordResetToken)
        .filter(models.PasswordResetToken.token_hash == token_hash, models.PasswordResetToken.used_at.is_(None))
        .first()
    )
    if not record or record.expires_at < datetime.now(timezone.utc):
        raise ValueError("Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not user:
        raise ValueError("User not found")

    user.password_hash = hash_password(new_password)
    record.used_at = datetime.now(timezone.utc)
    db.commit()

    log_event(
        db=db,
        action="auth.password_reset_completed",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={},
    )


def enable_mfa(db: Session, user: models.User, ip_address: str | None, user_agent: str | None):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    otpauth_url = totp.provisioning_uri(name=user.email, issuer_name=settings.mfa_issuer)

    backup_codes = [secrets.token_hex(4) for _ in range(8)]
    for code in backup_codes:
        db.add(models.MfaBackupCode(user_id=user.id, code_hash=_hash_token(code)))

    user.mfa_secret = secret
    user.mfa_enabled = False
    db.commit()

    log_event(
        db=db,
        action="auth.mfa_initiated",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={},
    )

    return secret, otpauth_url, backup_codes


def verify_mfa(db: Session, user: models.User, code: str, ip_address: str | None, user_agent: str | None):
    if not user.mfa_secret:
        raise ValueError("MFA not initiated")
    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(code, valid_window=1):
        raise ValueError("Invalid MFA code")
    user.mfa_enabled = True
    db.commit()

    log_event(
        db=db,
        action="auth.mfa_enabled",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={},
    )


def disable_mfa(db: Session, user: models.User, code: str, ip_address: str | None, user_agent: str | None):
    if not user.mfa_secret:
        raise ValueError("MFA not enabled")
    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(code, valid_window=1):
        if not _validate_backup_code(db, user, code):
            raise ValueError("Invalid MFA code")
    user.mfa_enabled = False
    user.mfa_secret = None
    db.query(models.MfaBackupCode).filter(models.MfaBackupCode.user_id == user.id).delete()
    db.commit()

    log_event(
        db=db,
        action="auth.mfa_disabled",
        entity_type="user",
        entity_id=str(user.id),
        actor_user_id=str(user.id),
        company_id=_resolve_primary_company(db, user),
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={},
    )


def _validate_backup_code(db: Session, user: models.User, code: str) -> bool:
    code_hash = _hash_token(code)
    record = (
        db.query(models.MfaBackupCode)
        .filter(
            models.MfaBackupCode.user_id == user.id,
            models.MfaBackupCode.code_hash == code_hash,
            models.MfaBackupCode.used_at.is_(None),
        )
        .first()
    )
    if not record:
        return False
    record.used_at = datetime.now(timezone.utc)
    db.commit()
    return True


def _resolve_primary_role(db: Session, user: models.User) -> str:
    membership = (
        db.query(models.CompanyMembership)
        .filter(models.CompanyMembership.user_id == user.id, models.CompanyMembership.is_primary.is_(True))
        .first()
    )
    if membership:
        return membership.role
    return "worker"


def _resolve_primary_company(db: Session, user: models.User) -> str | None:
    membership = (
        db.query(models.CompanyMembership)
        .filter(models.CompanyMembership.user_id == user.id, models.CompanyMembership.is_primary.is_(True))
        .first()
    )
    return str(membership.company_id) if membership else None


def uuid_from_time() -> str:
    return secrets.token_hex(16)
