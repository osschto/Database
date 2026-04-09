from datetime import date
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, Session, SQLModel, select


class Rental(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    user_id : Optional[int] = Field(foreign_key="user.id")
    car_id : Optional[int] = Field(foreign_key="car.id")
    date : date


class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    email: EmailStr
    hash_password : str
    phone_number : str
    driver_license_number : str
    role :  str = Field(default="user")

    cars : List["Car"] = Relationship(back_populates="users", link_model=Rental)


class Car(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True, index=True)
    category_id : Optional[int] = Field(foreign_key="category.id")
    brand : str
    model : str
    number : str
    available : bool = True

    category : Optional["Category"] = Relationship(back_populates="cars")
    users : List["User"] = Relationship(back_populates="cars", link_model=Rental)

class CarInfo(SQLModel, table=True):
    __tablename__ = "car_price"
    id : Optional[int] = Field(primary_key=True)
    brand : str
    model : str
    price : int


class Category(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    classification : str
    price : float
    
    cars : List["Car"] = Relationship(back_populates="category")

    @classmethod
    def set_categories(cls, db : Session):
        categories = [
            ("Эконом", 1000.0),
            ("Комфорт", 2000.0),
            ("Бизнес", 3500.0)]

        for classification, price in categories:
            exist = db.exec(select(cls).where(cls.classification == classification)).first()
            if not exist:
                db.add(cls(classification=classification, price=price))
                db.commit()


class Location(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    address : str