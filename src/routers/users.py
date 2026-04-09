from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date

from db.db import get_session
from models.model import User, Car, Rental
from models.schemas import UserLog, UserReg, UserGet, UserUpdate
from security.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["Users"])
current_user = None

@router.post("/reg", summary="Регистрация")
def reg(user : UserReg, db : Session = Depends(get_session)):
    user_db = User(**user.model_dump())
    user_db.hash_password = hash_password(user_db.hash_password)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return f"Пользователь <{user_db.name}> успешно зарегистрирован"

@router.post("/auth",  summary="Авторизация")
def auth(user : UserLog, db : Session = Depends(get_session)):
    user_db = db.exec(select(User).where(User.email == user.email)).first()
    if user_db.email == "admin@example.com":
        user_db.role = "admin"
        db.commit()
    if not user_db or not verify_password(user.hash_password, user_db.hash_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    global current_user
    current_user = user_db
    
    return f"Добро пожаловать, {user_db.name}"

@router.post("/{user_id}/cars/{car_id}", summary="Арендовать машину")
def rental_car(user_id : int, car_id : int, db : Session = Depends(get_session)):
    car_db = db.exec(select(Car).where(Car.id == car_id)).first()
    user_db = db.exec(select(User).where(User.id == user_id)).first()

    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    
    if not car_db:
        raise HTTPException(404, "Машина не найдена")

    if not car_db.available:
        raise HTTPException(400, "Машина недоступна для аренды")
    
    new_rental = Rental(
        user_id=user_id,
        car_id=car_id,
        date=date.today()
    )
    
    car_db.available = False

    db.add(new_rental)
    db.commit()

    return f"Машина: '{car_db.brand} {car_db.model}' арендована"

@router.get("/", response_model=List[UserGet], summary="Получить список всех пользователей")
def get_all_users(db : Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users

@router.put("/update/{user_id}", summary="Обновить информацию о пользователе")
def update_user(user_id : int, user : UserUpdate, db : Session = Depends(get_session)):
    user_db = db.exec(select(User).where(User.id == user_id)).first()
    if current_user.role != "admin":
        raise HTTPException(403, "Нет прав доступа")
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    
    user_db.email = user.email
    db.commit()

    return f"Данные пользователя <{user_db.name}> обновлены"

@router.delete("/delete/{user_id}", summary="Удалить пользователя")
def delete_user(user_id : int, db : Session = Depends(get_session)):
    user_db = db.exec(select(User).where(User.id == user_id)).first()
    if current_user.role != "admin":
        raise HTTPException(403, "Нет прав доступа")
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    
    db.delete(user_db)
    db.commit()

    return f"Пользователь <{user_db.name}> успешно удален"