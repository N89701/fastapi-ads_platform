from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
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
    category_id = int
    

class AdvertisementCreate(AdvertisementBase):
    category_id: int
    photos: List[PhotoCreate]


class AdvertisementRead(AdvertisementBase):
    id: int
    category_id: CategoryRead
    photos: List[PhotoBase]

    class Config:
        orm_mode = True


class RecallCreate(BaseModel):
    advertisement_id: int
    text: str


class RecallRead(BaseModel):
    id: int
    author_id: UserRead
    advertisement_id: AdvertisementCreate
    text: str


class ComplaintCreate(BaseModel):
    advertisement_id: int
    text: str


class ComplaintRead(BaseModel):
    id: int
    author_id: UserRead
    advertisement_id: AdvertisementCreate
    text: str
