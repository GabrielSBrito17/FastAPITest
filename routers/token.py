from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from crud.user import create_user as db_create_user, get_user_by_username as db_get_user_by_username
from security.token import create_access_token, verify_user, get_user_permissions
from security.security import Security, UserToken

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = verify_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": get_user_permissions(user)},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create_user")
async def create_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    db_user = db_get_user_by_username(db, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = Security.get_password_hash(password)
    return db_create_user(db, username=username, email=email, password=hashed_password)

@router.get("/users/me")
async def read_users_me(current_user: UserToken = Depends(Security.get_current_user)):
    return current_user
