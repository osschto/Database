import uvicorn
from fastapi import FastAPI

from db.db import create_db_and_tables
from routers import users, cars, locations, categories

app = FastAPI()

app.include_router(users.router)
app.include_router(cars.router)
app.include_router(locations.router)
app.include_router(categories.router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", reload=True)