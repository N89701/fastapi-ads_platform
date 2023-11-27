from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_async_session
from .models import Advertisement, Category, Group, Photo, Recall, Complaint
from .schemas import (
    CategoryCreate, CategoryRead, GroupCreate, GroupRead, ComplaintRead,
    RecallRead, RecallCreate, ComplaintCreate, AdvertisementCreate
)
from users.auth import auth_backend
from users.manager import get_user_manager
from users.models import User


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
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete group"
        )
    group = delete(Group).where(Group.id == group_id)
    await session.execute(group)
    await session.commit()
    return {"status": "success"}


router_ads = APIRouter(
    tags=['ads'],
    prefix='/ads',
)


@router_ads.get('/')
async def get_ads(
    session: AsyncSession = Depends(get_async_session),
    page: int = 1,
    page_size: int = 5,
    category_id: int = None,
    type: str = None,
    sort_by_category: bool = False
):
    query = select(Advertisement).options(selectinload(Advertisement.photos))

    if category_id is not None:
        query = query.filter(Advertisement.category_id == category_id)
    if type is not None:
        query = query.filter(Advertisement.type == type)

    if sort_by_category:
        query = query.order_by(Advertisement.category_id)

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    ads = await session.execute(query)
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
    ad = insert(Advertisement).values(**ad_data).returning(Advertisement.id)
    result = await session.execute(ad)
    advertisement_id = result.scalar()

    photos_objects = []
    for photo_data in photos_data:
        photo_data["advertisement_id"] = advertisement_id
        photo = insert(Photo).values(**photo_data)
        result = await session.execute(photo)
        photos_objects.append(result.scalar())

    await session.commit()
    return {
        "status": "success",
        "advertisement": advertisement_id,
        "photos": photos_objects
    }


@router_ads.get('/{id}/')
async def get_ad(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    advertisement = await session.execute(
        select(Advertisement).options(
            selectinload(Advertisement.photos)
        ).filter(Advertisement.id == id).limit(1)
    )
    advertisement = advertisement.scalar_one_or_none()
    if advertisement is None:
        raise HTTPException(
            status_code=404, detail="This advertisement is not exists"
        )
    return advertisement


@router_ads.patch('/{id}/')
async def update_ad(
    id: int,
    request: AdvertisementCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    advertisement = await session.execute(
        select(Advertisement).where(Advertisement.id == id)
    )
    advertisement = advertisement.scalar()

    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    if not user.is_superuser or user.id != advertisement.author_id:
        raise HTTPException(
            status_code=403,
            detail="Only the author can update the advertisement"
        )
    update_data = request.dict(exclude_unset=True)
    photos_data = update_data.pop('photos')
    await session.execute(update(Advertisement).where(
        Advertisement.id == id
    ).values(update_data))
    photos_objects = []
    await session.execute(
        delete(Photo).where(Photo.advertisement_id == id)
    )
    for photo_data in photos_data:
        photo_data["advertisement_id"] = id
        photo = insert(Photo).values(**photo_data)
        result = await session.execute(photo)
        photos_objects.append(result.scalar())
    await session.commit()
    return {"status": "success"}


@router_ads.delete('/{id}/')
async def delete_ad(
    id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    advertisement = await session.execute(
        select(Advertisement).where(Advertisement.id == id)
    )
    advertisement = advertisement.scalar()
    if not (user.is_superuser or (
        advertisement and advertisement.author_id == user.id)
    ):
        raise HTTPException(
            status_code=403,
            detail="Only author or admin can delete theadvertisement"
        )
    advertisement = delete(Advertisement).where(Advertisement.id == id)
    await session.execute(advertisement)
    await session.commit()
    return {"status": "success"}


router_recalls = APIRouter(
    tags=['recalls'],
    prefix='/ads/{ad_id}',
)


@router_recalls.get('/', response_model=List[RecallRead])
async def get_recalls(
    ad_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    recalls = await session.execute(
        select(Recall).filter(Recall.advertisement_id == ad_id).limit(10)
    )
    recalls = recalls.scalar().all()
    return recalls


@router_recalls.post('/')
async def create_recall(
    ad_id: int,
    request: RecallCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    recall_data = request.dict()
    recall_data["author_id"] = user.id
    recall_data["advertisement_id"] = ad_id
    recall = insert(Recall).values(**recall_data)
    await session.execute(recall)
    await session.commit()
    return {"status": "success"}


@router_recalls.delete('/{id}/')
async def delete_recall(
    ad_id: int,
    id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    recall = await session.execute(
        select(Recall).where(Recall.id == id)
    )
    recall = recall.scalar()
    if not (user.is_superuser or (
        recall and recall.author_id == user.id)
    ):
        raise HTTPException(
            status_code=403,
            detail="Only author or admin can delete recall"
        )
    recall = delete(Recall).where(Recall.id == id)
    await session.execute(recall)
    await session.commit()
    return {"status": "success"}


router_complaints = APIRouter(
    tags=['complaints'],
    prefix='/ads/{ad_id}',
)


@router_complaints.get('/', response_model=List[ComplaintRead])
async def get_complaints(
    ad_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only author or admin can delete recall"
        )
    complaints = await session.execute(
        select(Complaint).filter(Complaint.advertisement_id == ad_id).limit(10)
    )
    complaints = complaints.scalar().all()
    return complaints


@router_complaints.post('/')
async def create_complaint(
    ad_id: int,
    request: ComplaintCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    complaint_data = request.dict()
    complaint_data["author_id"] = user.id
    complaint_data["advertisement_id"] = ad_id
    complaint = insert(Complaint).values(**complaint_data)
    await session.execute(complaint)
    await session.commit()
    return {"status": "success"}


@router_complaints.delete('/{id}/')
async def delete_complaints(
    ad_id: int,
    id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    complaint = await session.execute(
        select(Complaint).where(Complaint.id == id)
    )
    complaint = complaint.scalar()
    if not (user.is_superuser or (
        complaint and complaint.author_id == user.id)
    ):
        raise HTTPException(
            status_code=403,
            detail="Only author or admin can delete recall"
        )
    complaint = delete(Complaint).where(Complaint.id == id)
    await session.execute(complaint)
    await session.commit()
    return {"status": "success"}
