from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from users.schemas import UserRead


class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str


class GroupCreate(BaseModel):
    title: str
    description: str
    avatar: str


class GroupRead(BaseModel):
    id: int
    title: str
    description: str
    avatar: str

    class Config:
        orm_mode = True


class AdvertisementType(str, Enum):
    SELL = 'sell'
    BUY = 'buy'
    SERVICE = 'service'


class PhotoBase(BaseModel):
    url: str


class PhotoCreate(BaseModel):
    url: str


class AdvertisementBase(BaseModel):
    title: str
    type: AdvertisementType
    description: str
    price: int
    group_id: Optional[int]
    # category_id: int


class AdvertisementCreate(AdvertisementBase):
    photos: List[PhotoCreate]
    category_id: int


class AdvertisementRead(AdvertisementBase):
    id: int
    photos: List[PhotoBase]
    author_id: UserRead
    category_id: int

    class Config:
        orm_mode = True


class RecallCreate(BaseModel):
    text: str


class RecallRead(BaseModel):
    id: int
    author_id: UserRead
    advertisement_id: AdvertisementCreate
    text: str


class ComplaintCreate(BaseModel):
    text: str


class ComplaintRead(BaseModel):
    id: int
    author_id: UserRead
    advertisement_id: AdvertisementCreate
    text: str
