from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.db import get_session
from models.model import Category
from models.schemas import CategoryGet

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryGet], summary="Получить список всех категорий")
def get_all_categories(db : Session = Depends(get_session)):
    categories = db.exec(select(Category)).all()
    return categories   