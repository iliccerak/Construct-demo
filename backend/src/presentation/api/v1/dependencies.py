from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from application.auth.rbac import has_permission
from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence import models
from infrastructure.security.jwt_service import decode_token

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(creds.credentials)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user, payload


def require_permission(permission: str):
    def _checker(
        user_payload=Depends(get_current_user),
    ):
        user, payload = user_payload
        role = payload.get("role", "worker")
        if not has_permission(role, permission):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user, payload

    return _checker


def require_company_scope(
    request: Request,
    user_payload=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user, payload = user_payload
    company_id = request.path_params.get("company_id")
    if payload.get("role") != "super_admin":
        if payload.get("company_id") != company_id:
            raise HTTPException(status_code=403, detail="Company scope mismatch")
        membership = (
            db.query(models.CompanyMembership)
            .filter(
                models.CompanyMembership.user_id == user.id,
                models.CompanyMembership.company_id == company_id,
            )
            .first()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Company membership required")
    return user, payload
