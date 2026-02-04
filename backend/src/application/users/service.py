from sqlalchemy.orm import Session

from infrastructure.persistence import models


def get_current_user(db: Session, user_id: str) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user
