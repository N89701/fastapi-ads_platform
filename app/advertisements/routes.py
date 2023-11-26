from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, selectinload
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from fastapi_users import FastAPIUsers
from fastapi.exceptions import HTTPException
from typing import List
import base64

from database import get_async_session, get_session
from .models import Advertisement, Category, Group, Photo
from .schemas import (
    CategoryCreate, CategoryRead, GroupCreate, GroupRead, AdvertisementRead,
    AdvertisementCreate
)
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

@router_categories.get('/', response_model=List[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    categories = await session.execute(select(Category))
    category_list = categories.scalars().all()
    return category_list


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


@router_groups.get('/', response_model=List[GroupRead])
async def get_groups(session: AsyncSession = Depends(get_async_session)):
    groups = await session.execute(select(Group))
    groups_list = groups.scalars().all()
    return groups_list


@router_groups.get('/{id}/', response_model=GroupRead)
async def get_group(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    group = await session.execute(
        select(Group).filter(Group.id == id).limit(1)
    )
    group = group.scalar_one_or_none()
    if group is None:
        raise HTTPException(status_code=404, detail="This group is not exists")
    return group


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


@router_groups.delete('/{group_id}/')
async def delete_group(
    group_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admin can delete group")
    group = delete(Group).where(Group.id == group_id)
    await session.execute(group)
    await session.commit()
    return {"status": "success"}


router_ads = APIRouter(
    tags=['ads'],
    prefix='/ads',
)


@router_ads.get('/', response_model=List[AdvertisementRead])
async def get_ads(session: AsyncSession = Depends(get_async_session)):
    ads = await session.execute(select(Advertisement))
    ads_list = ads.scalars().all()
    return ads_list


@router_ads.post('/')
async def create_advertisement(
    request: AdvertisementCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    ad_data = request.dict()
    photos_data = ad_data.pop('photos')

    ad_data["author_id"] = user.id

    # Create the advertisement
    ad = insert(Advertisement).values(**ad_data).returning(Advertisement.id)
    result = await session.execute(ad)
    advertisement_id = result.scalar()
    # Create photos and associate them with the advertisement
    photos_objects = []
    for photo_data in photos_data:
        print(photos_data)
        # photo_url = base64.b64decode(photo_data["url"]).decode("utf-8")
        photo_data["advertisement_id"] = advertisement_id
        # photo_data["url"] = photo_url
        photo = insert(Photo).values(**photo_data)
        result = await session.execute(photo)
        photos_objects.append(result.scalar())

    # Commit the transaction
    await session.commit()

    # Return success response
    return {
        "status": "success",
        "advertisement": advertisement_id,
        "photos": photos_objects
    }
