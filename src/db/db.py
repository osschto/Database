from sqlmodel import SQLModel, Session, create_engine, text
from models.model import Category

engine = create_engine("sqlite:///src/db/database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
            Category.set_categories(session)
            
            session.exec(text("DROP TABLE IF EXISTS car_price"))
            session.exec(text('''
            CREATE VIEW car_price AS
            SELECT c.id, c.brand, c.model, cat.price
            FROM Car c
            JOIN Category cat ON c.category_id = cat.id'''))

            session.commit()

def get_session():
    with Session(engine) as session:
        yield session