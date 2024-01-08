from sqlalchemy.orm import Session
from datetime import timedelta
from crud.user import get_user_by_username
from .security import Security

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return Security.create_access_token(
        data, expires_delta=expires_delta
    )

def verify_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    print(user)
    if not user or not Security.verify_password(password, user.password):
        return None
    return user

def get_user_permissions(user):
    return ["is_superuser"] if user.is_superuser else []
