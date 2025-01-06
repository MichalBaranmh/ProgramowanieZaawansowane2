from typing import Union, Annotated

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from dbActions import init_db, db_writeRateFromRangeofDates, Rate

from requests import request
from datetime import date

app = FastAPI()

#Kazda aplikacja moze komunikowac sie z naszym api
origins = [
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

#wyswietlanie walut z bazy danych
#@app.get("/currencies")
#def read_AvailableCurrencies():
#    return{"toBeImplemented":"1"}
#
##wyswietlanie kursow z bazy danych 
#@app.get("/currencies/{date}")
#def read_AvailableCurrenciesFromGivenDay():
#    return{"toBeImplemented":"2"}

#zdobywanie kursów z bazy danych Narodowego Banku Polskiego
@app.post("/currencies/fetch/{code}/{startDate}/{endDate}")
def write_FeedDatabase(code:str,startDate:str,endDate:str):
    try:
        db_writeRateFromRangeofDates(code,startDate,endDate)
        return "OK"
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

