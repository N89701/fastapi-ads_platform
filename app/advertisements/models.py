import datetime


from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()



class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    admin_id = Column(Integer,  ForeignKey("user.id"))
    description = Column(String)
    avatar = Column(String)


class Advertisement(Base):
    # from users.models import User
    __tablename__ = "advertisement"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    author_id = Column(Integer,  ForeignKey("user.id"))
    description = Column(String)
    pub_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    price = Column(Integer)
    group_id = Column(Integer, ForeignKey("group.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    is_active = Column(Boolean)


class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    advertisement_id = Column(Integer, ForeignKey('advertisement.id'))
    # advertisement = relationship("Advertisement", back_populates="photos")


class Recall(Base):
    __tablename__ = "recalls"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer,  ForeignKey("user.id"))
    advertisement_id = Column(Integer, ForeignKey("advertisement.id"))
    text = Column(String)


class Complaint(Base):
    __tablename__ = "complaint"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer,  ForeignKey("user.id"))
    advertisement_id = Column(Integer, ForeignKey("advertisement.id"))
    text = Column(String)
