from advertisements.models import Base

from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends

from users.auth import auth_backend
from users.models import User
from users.manager import get_user_manager
from users.schemas import UserRead, UserCreate

app = FastAPI()
# Base.metadata.create_all(bind=engine)


