from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.users.service import get_current_user as fetch_user
from presentation.api.v1.dependencies import get_current_user, get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user_payload=Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = user_payload
    try:
        current = fetch_user(db, str(user.id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "id": str(current.id),
        "email": current.email,
        "first_name": current.first_name,
        "last_name": current.last_name,
        "email_verified_at": current.email_verified_at,
    }
