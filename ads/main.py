from ads.advertisements.models import Base

from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends

from ads.users.auth import auth_backend
from ads.users.models import User
from ads.users.manager import get_user_manager
from ads.users.schemas import UserRead, UserCreate

ads = FastAPI()
# Base.metadata.create_all(bind=engine)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

ads.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

ads.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@ads.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.first_name} {user.last_name}"


@ads.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"
