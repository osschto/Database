from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.db import get_session
from models.model import Location
from models.schemas import LocationAdd, LocationGet, LocationUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("/add", summary="Добавить новый офис")
def add_location(location : LocationAdd, db : Session = Depends(get_session)):
    location_db = Location(**location.model_dump())
    db.add(location_db)
    db.commit()
    db.refresh(location_db)

    return f"Офис по адресу <{location_db.address}> успешно добавлен"


@router.get("/", response_model=List[LocationGet], summary="Получить список адресов всех офисов")
def get_all_locations(db : Session = Depends(get_session)):
    locations = db.exec(select(Location)).all()
    return locations


@router.put("/update/{loc_id}", summary="Обновить информацию об офисе")
def update_location(loc_id : int, loc : LocationUpdate , db : Session = Depends(get_session)):
    loc_db = db.exec(select(Location).where(Location.id == loc_id)).first()
    if not loc_db:
        raise HTTPException(404, "Офис не найден")
    
    loc_db.address = loc.address
    db.commit()
    db.refresh(loc_db)
    
    return f"Данные офиса по адресу <{loc_db.address}> успешно обновлены"
    

@router.delete("/delete/{loc_id}", summary="Удалить информацию об офисе")
def delete_location(loc_id : int, db : Session = Depends(get_session)):
    loc_db = db.exec(select(Location).where(Location.id == loc_id)).first()
    if not loc_db:
        raise HTTPException(404, "Офис не найден")
    
    db.delete(loc_db)
    db.commit()
    
    return f"Офис по адресу <{loc_db.address}> успешно удален"