from sqlalchemy.orm import Session
from .models import Category, Group, Advertisement, Complaint, Recall, Photo


def create_category(db: Session, name):
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category