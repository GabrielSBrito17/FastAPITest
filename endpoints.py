# from token import create_jwt_token, get_current_user
# from controllers import fake_users_db, User
# from main import app
# from fastapi import Depends, HTTPException, status
# from passlib.context import CryptContext
#
# # Configuração do Bcrypt para hash de senhas
# PASSWORD_HASH = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# # Endpoint para obter informações do usuário atual
# @app.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
#
# # Endpoint para autenticação e geração de token JWT
# @app.post("/token")
# async def login_for_access_token(username: str, password: str):
#     user = fake_users_db.get(username)
#     if user and PASSWORD_HASH.verify(password, user.password):
#         token_data = {"sub": username, "scopes": ["me"]}
#         return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}
#
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid username or password",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
# # Endpoint para criar um novo usuário
# @app.post("/users/", response_model=User)
# async def create_user(user: User, current_user: User = Depends(get_current_user)):
#     if current_user["role"] != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only admin users can create new users",
#         )
#     fake_users_db[user.username] = user
#     return user
#
# # Endpoint para ler informações de um usuário
# @app.get("/users/{username}", response_model=User)
# async def read_user(username: str, current_user: User = Depends(get_current_user)):
#     if current_user["role"] == "admin" or current_user["username"] == username:
#         user = fake_users_db.get(username)
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found",
#             )
#         return user
#
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="You don't have access to this user's information",
#     )
#
# # Endpoint para atualizar informações de um usuário
# @app.put("/users/{username}", response_model=User)
# async def update_user(username: str, new_data: User, current_user: User = Depends(get_current_user)):
#     if current_user["role"] == "admin" or current_user["username"] == username:
#         user = fake_users_db.get(username)
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found",
#             )
#         user.__dict__.update(new_data.__dict__)
#         return user
#
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="You don't have access to update this user's information",
#     )
#
# # Endpoint para deletar um usuário
# @app.delete("/users/{username}", response_model=User)
# async def delete_user(username: str, current_user: User = Depends(get_current_user)):
#     if current_user["role"] == "admin" or current_user["username"] == username:
#         user = fake_users_db.pop(username, None)
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found",
#             )
#         return user
#
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="You don't have access to delete this user",
#     )