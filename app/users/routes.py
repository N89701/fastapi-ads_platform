from app.advertisements.models import Base

from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends

from app.users.auth import auth_backend
from app.users.models import User
from app.users.manager import get_user_manager
from app.users.schemas import UserRead, UserCreate


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.first_name} {user.last_name}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"