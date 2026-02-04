from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from application.auth import service
from application.auth.schemas import (
    EmailVerificationRequest,
    ForgotPasswordRequest,
    LoginRequest,
    MfaEnableResponse,
    MfaVerifyRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from presentation.api.v1.dependencies import get_current_user, get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db), http_request: Request = None):
    try:
        user = service.register_user(db, request, http_request.client.host if http_request else None, http_request.headers.get("user-agent") if http_request else None)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"id": str(user.id), "email": user.email}


@router.post("/verify-email")
def verify_email(request: EmailVerificationRequest, db: Session = Depends(get_db), http_request: Request = None):
    try:
        service.verify_email(db, request.token, http_request.client.host if http_request else None, http_request.headers.get("user-agent") if http_request else None)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "verified"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db), http_request: Request = None):
    try:
        access_token, refresh_token = service.login_user(
            db,
            request.email,
            request.password,
            request.mfa_code,
            http_request.client.host if http_request else None,
            http_request.headers.get("user-agent") if http_request else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=900)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db: Session = Depends(get_db), http_request: Request = None):
    try:
        access_token, refresh_token = service.refresh_session(
            db,
            request.refresh_token,
            http_request.client.host if http_request else None,
            http_request.headers.get("user-agent") if http_request else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=900)


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db), http_request: Request = None):
    service.initiate_password_reset(
        db,
        request.email,
        http_request.client.host if http_request else None,
        http_request.headers.get("user-agent") if http_request else None,
    )
    return {"status": "sent"}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db), http_request: Request = None):
    try:
        service.reset_password(
            db,
            request.token,
            request.new_password,
            http_request.client.host if http_request else None,
            http_request.headers.get("user-agent") if http_request else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "reset"}


@router.post("/mfa/enable", response_model=MfaEnableResponse)
def mfa_enable(user_payload=Depends(get_current_user), db: Session = Depends(get_db), http_request: Request = None):
    user, _ = user_payload
    secret, otpauth_url, backup_codes = service.enable_mfa(
        db,
        user,
        http_request.client.host if http_request else None,
        http_request.headers.get("user-agent") if http_request else None,
    )
    return MfaEnableResponse(secret=secret, otpauth_url=otpauth_url, backup_codes=backup_codes)


@router.post("/mfa/verify")
def mfa_verify(request: MfaVerifyRequest, user_payload=Depends(get_current_user), db: Session = Depends(get_db), http_request: Request = None):
    user, _ = user_payload
    try:
        service.verify_mfa(
            db,
            user,
            request.code,
            http_request.client.host if http_request else None,
            http_request.headers.get("user-agent") if http_request else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "enabled"}


@router.post("/mfa/disable")
def mfa_disable(request: MfaVerifyRequest, user_payload=Depends(get_current_user), db: Session = Depends(get_db), http_request: Request = None):
    user, _ = user_payload
    try:
        service.disable_mfa(
            db,
            user,
            request.code,
            http_request.client.host if http_request else None,
            http_request.headers.get("user-agent") if http_request else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "disabled"}
