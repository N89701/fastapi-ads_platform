from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    first_name: str
    last_name: str
    contact: str
    # is_active: bool = True
    # is_superuser: bool = False
    # is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    first_name: str
    last_name: str
    contact: str
    password: str
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False