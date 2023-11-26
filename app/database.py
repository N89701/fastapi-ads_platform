from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from fastapi import Depends

from advertisements.models import Base


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ads"

# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def get_session():
#     session = Session()
#     try:
#         yield session
#     finally:
#         session.close()


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# def get_session():
#     session = Session()
#     try:
#         yield session
#     finally:
#         session.close()


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
    

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def download_categories(session: Session = Depends(get_async_session)):
    from advertisements.models import Category
    # category_names = [
    #     "Одежда",
    #     "Обувь",
    #     "Аксессуары и украшения",
    #     "Бытовая техника",
    #     "Компьютеры и гаджеты",
    #     "Мебель",
    #     "Хобби и развлечения",
    #     "Спорт",
    #     "Музыка",
    #     "Коллекционирование",
    #     "Красота и здоровье",
    #     "Ремонтные услуги",
    #     "Автомобили",
    #     "Мотоциклы",
    #     "Резюме",
    #     "Вакансии",
    #     "Недвижимость"
    #     ]
    # for category in category_names:
    obj = Category(name="")
    session.add(obj)
    session.commit()
    session.refresh(obj)
    print("Объекты успешно загружены")


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
