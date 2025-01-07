from typing import Optional, List
from datetime import date
import requests
from sqlalchemy import URL
from sqlmodel import Field, SQLModel, create_engine, Session, Relationship, select
from fastapi import HTTPException, status

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

#domyslny wsad z walutami
currency_codes =[
    {"code":"USD"},
    {"code":"EUR"},
    {"code":"JPY"},
    {"code":"CHF"},
    {"code":"CNY"},
]

#klasa z kodami walut
class CurrencyCode (SQLModel, table=True):
    CurrencyId: int | None = Field(default=None,primary_key=True)
    code: str = Field(index=True,unique=True)
    #relacje
    rates: List["Rate"] = Relationship(back_populates="currency")
    transactions: List["Transaction"] = Relationship(back_populates="currency")

#klasa z transakcjami, kurs mozna pobrac tylko z dni, ktorych nie ma w bazie danych
class Transaction (SQLModel, table=True):
    TransactionId: int | None = Field(default=None, primary_key=True)
    CurrencyId: int = Field(foreign_key="currencycode.CurrencyId")
    RateId: int = Field(foreign_key="rate.RateId")
    effectiveDate: date
    #relacje
    rate: Optional["Rate"] = Relationship(back_populates="transactions")
    currency: Optional["CurrencyCode"] = Relationship(back_populates="transactions")

#klasa z kursem waluty
class Rate(SQLModel, table=True):
    RateId: int | None = Field(default=None, primary_key=True)
    CurrencyId: int = Field(foreign_key="currencycode.CurrencyId")
    effectiveDate: date
    mid: float
    #relacje
    transactions: List["Transaction"] = Relationship(back_populates="rate")
    currency: Optional["CurrencyCode"] = Relationship(back_populates="rates")


engine = create_engine(DATABASE_URL, echo=True)

try:
    with engine.connect() as connn:
        print("Connection ok")
except Exception as e:
    print(f"Err: {e}")


#inicjalizacja tabel
def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for curr in currency_codes:
            exist = session.exec(
                select(CurrencyCode).where(CurrencyCode.code==curr["code"])
            ).first()
            if not exist:
                session.add(CurrencyCode(**curr))
        session.commit()


#czytanie dostepnych walut z tabeli currencycode
def db_readCurrencyCode():
    with Session(engine) as session:
        currencies = session.exec(select(CurrencyCode)).all()
        return[{currency.code}for currency in currencies]

#czytanie dostepnych kursow walut z konkretnego dnia
def db_readRates(date:str) -> List[dict]:
    with Session(engine) as session:
        query = (select(Rate,CurrencyCode.code)
                .join(CurrencyCode,Rate.CurrencyId==CurrencyCode.CurrencyId)
                .where(Rate.effectiveDate==date))
        results = session.exec(query).all()

        return[
            {
                "RateId": rate.RateId,
                "code": code,
                "effectiveDate": rate.effectiveDate,
                "mid": rate.mid
            } for rate, code in results
        ]

#dodawanie rekordow do tabeli rate
def db_writeRateFromRangeofDates(code: str,dataPoczatkowa:str,dataKoncowa:str):
    with Session(engine) as session:
        currency = session.exec(select(CurrencyCode).where(CurrencyCode.code == code)).first()
        if not currency:
            raise HTTPException(status_code=404,detail="Currency code is not valid")
        
        r = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/A/{code}/{dataPoczatkowa}/{dataKoncowa}/?format=json")
        content = r.json()
        
        for rate_data in content["rates"]:
            rate_date = rate_data["effectiveDate"]
            mid_rate = rate_data["mid"]
            
            existing_transaction = session.exec(select(Transaction).where(Transaction.CurrencyId == currency.CurrencyId, Transaction.effectiveDate == rate_date)).first()
        
            if not existing_transaction:
                new_rate = Rate(
                    CurrencyId=currency.CurrencyId,
                    effectiveDate=rate_date,
                    mid=mid_rate
                )
                session.add(new_rate)
                session.commit()

                new_transaction = Transaction(
                    CurrencyId=currency.CurrencyId,
                    RateId=new_rate.RateId,
                    effectiveDate=rate_date
                )
                session.add(new_transaction)
                session.commit()


if __name__ == "__main.py__":
    init_db()
    db_writeRateFromRangeofDates()
