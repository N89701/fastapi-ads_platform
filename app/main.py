from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends


from users.auth import auth_backend
from users.models import User
from users.manager import get_user_manager
from users.schemas import UserRead, UserCreate
from advertisements.routes import router_categories, router_groups


app = FastAPI(title="Advertisement app")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()

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

app.include_router(router_categories)
app.include_router(router_groups)

