from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from db.db import get_session
from models.model import Car, Category
from models.schemas import CarAdd, CarGet, CarByCategory, CarCountByCategory, CarUpdate

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.post("/add", summary="Добавить новую машину")
def add_car(car : CarAdd ,db : Session = Depends(get_session)):
    category_db = db.exec(select(Category).where(Category.id == car.category_id)).first()
    if not category_db:
        raise HTTPException(422, "Категория с указанным id не найдена")

    car_db = Car(**car.model_dump())
    db.add(car_db)
    db.commit()
    db.refresh(car_db)

    return f"Машина <{car_db.brand} {car_db.model}> была успешно добавлена"

@router.get("/get_all_available", response_model=List[CarGet], summary="Получить список всех доступных для аренды машин")
def get_all_available_cars(db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.available == True)).all()
    return car_db

@router.get("/get/{car_id}", response_model=CarGet, summary="Получить машину по id")
def get_car_by_id(car_id : int, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()
    if not car_db:
        raise HTTPException(404, "Машина не найдена")

    return car_db

@router.get("/by_category/{category_class}", response_model=List[CarByCategory], summary="Получить список машин по конкретной категории")
def get_cars_by_category(category_class : str, db : Session = Depends(get_session)):
    category_db = db.exec(select(Category).where(Category.classification == category_class)).first()
    if not category_db:
        raise HTTPException(404, "Категория не найдена")
    
    cars = db.exec(
            select(Car)
            .join(Category, Car.category_id == Category.id)
            .where(Category.classification == category_class)).all()
    
    return [
        CarByCategory(
            category=category_db.classification,
            brand=car.brand,
            model=car.model,
            number=car.number
        )
        for car in cars
    ]

@router.get("/count_by_category/{category_class}", response_model=CarCountByCategory, summary="Получить кол-во машин в конкретной категории")
def getcars_count_by_category(category_class : str, db: Session = Depends(get_session)):
    category_db = db.exec(select(Category).where(Category.classification == category_class)).first()
    if not category_db:
        raise HTTPException(404, "Категория не найдена")

    cars = db.exec(select(Category.classification,func.count(Car.id).label("cars_count"))
        .join(Car, Car.category_id == Category.id, isouter=True)
        .where(Category.classification == category_class)
        .group_by(Category.classification)).first()
    cars_count = cars.cars_count
    
    return CarCountByCategory(category=category_db.classification, car_count=cars_count)

@router.put("/update/{car_id}", summary="Обновить информацию о машине")
def update_car(car_id : int, car : CarUpdate, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()
    if not car_db:
        raise HTTPException(404, "Машина не найдена")

    car_db.available = car.available
    car_db.number = car.number
    db.commit()
    db.refresh(car_db)

    return f"Информация о машине <{car_db.brand} {car_db.model}> была обновлена"

@router.delete("/delete/{car_id}", summary="Удалить информацию о машине")
def delete_car(car_id : int, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()
    if not car_db:
        raise HTTPException(404, "Машина не найдена")

    db.delete(car_db)
    db.commit()

    return f"Машина <{car_db.brand} {car_db.model}> была успешно удалена"
