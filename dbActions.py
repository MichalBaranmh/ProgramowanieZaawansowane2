from typing import Optional
from datetime import date

from sqlalchemy import URL
from sqlmodel import Field, SQLModel, create_engine

#tworzenie connectionstringa dla polaczenia z DB
db_url = URL.create(
    "postgresql",
    username="postgres",
    password="postgres",
    host="postgres",
    database="postgres",
    port=5432,
)

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

#klasa z kursem waluty
class Rate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str
    effectiveDate: date
    mid: float

engine = create_engine(DATABASE_URL, echo=True)

try:
    with engine.connect() as connn:
        print("Connection ok")
except Exception as e:
    print(f"Err: {e}")

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main.py__":
    init_db()

