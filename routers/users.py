from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud
from sqlalchemy.exc import IntegrityError
from schemas.schemas import User, UserCreate, UserUpdate
from database.database import get_db
import crud.user as user_crud
from security.security import Security, UserToken, ACCESS_TOKEN_EXPIRE_MINUTES
from security.token import verify_user, create_access_token, get_user_permissions

router = APIRouter(prefix="/users")

@router.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Security.create_access_token(
        data={"sub": user.username, "scopes": get_user_permissions(user)},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = Security.get_password_hash(user.password)
    user.password = hashed_password
    try:
        return user_crud.create_user(db=db, username=user.username, email=user.email, password=user.password, is_active=user.is_active, is_superuser=user.is_superuser)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

@router.get("/all", response_model=List[User])
def get_all_users(db: Session = Depends(get_db), current_user: UserToken = Depends(Security.get_current_user)):
    is_superuser = "is_superuser" in current_user.scopes
    if "is_superuser" not in current_user.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    users = user_crud.get_all_users(db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not is_superuser and current_user.username != users.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserToken = Depends(Security.get_current_user)):
    is_superuser = "is_superuser" in current_user.scopes
    if "is_superuser" not in current_user.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not is_superuser and current_user.username != db_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return db_user

@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK, description="User updated successfully")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserToken = Depends(Security.get_current_user)):
    if "is_superuser" not in current_user.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not ("is_superuser" in current_user.scopes or current_user.username == db_user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    updated_user = user_crud.update_user(db=db, user_id=user_id, user_update=user_update)
    return updated_user

@router.delete("/{user_id}", response_model=User, status_code=status.HTTP_200_OK, description="User deleted successfully")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserToken = Depends(Security.get_current_user)):
    if "is_superuser" not in current_user.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not ("is_superuser" in current_user.scopes or current_user.username == db_user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    user_crud.delete_user(db=db, user_id=user_id)
    return db_user
