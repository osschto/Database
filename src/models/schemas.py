from pydantic import BaseModel, EmailStr

class UserReg(BaseModel):
    name : str
    email : EmailStr
    hash_password : str
    phone_number : str
    driver_license_number : str

class UserLog(BaseModel):
    email : EmailStr
    hash_password : str

class UserGet(BaseModel):
    name : str
    email : EmailStr

class UserUpdate(BaseModel):
    email : EmailStr


class CarAdd(BaseModel):
    category_id : int
    brand : str
    model : str
    number : str
    available : bool

class CarUpdate(BaseModel):
    number : str
    available : bool

class CarGet(BaseModel):
    id : int
    brand : str
    model : str
    number : str    

class CarByCategory(BaseModel):
    category : str
    brand : str
    model : str
    number : str

class CarCountByCategory(BaseModel):
    category : str
    car_count : int

class LocationAdd(BaseModel):
    address : str

class LocationUpdate(BaseModel):
    address : str

class LocationGet(BaseModel):
    address : str

class CategoryGet(BaseModel):
    classification : str
    price : float