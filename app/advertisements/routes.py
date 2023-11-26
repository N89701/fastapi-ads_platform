from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from fastapi_users import FastAPIUsers
from fastapi.exceptions import HTTPException

from database import get_async_session
from .crud import create_category
from .models import Category, Group
from .schemas import CategoryCreate, CategoryRead, GroupCreate
from users.schemas import UserRead
from users.models import User
from users.manager import get_user_manager
from users.auth import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()


router_categories = APIRouter(
    tags=['categories'],
    prefix='/categories',
)


@router_categories.post('/')
async def create_category(
    request: CategoryCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not admin")
    category = insert(Category).values(**request.dict())
    await session.execute(category)
    await session.commit()
    return {"status": "success"}


router_groups = APIRouter(
    tags=['groups'],
    prefix='/groups',
)


@router_groups.post('/')
async def create_group(
    request: GroupCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    group_data = request.dict()
    group_data["admin_id"] = user.id
    group = insert(Group).values(**group_data)
    await session.execute(group)
    await session.commit()
    return {"status": "success"}