from typing import Union

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from dbActions import init_db

from requests import request


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
@app.post("/currencies/fetch")
def write_FeedDatabase():
    return {"toBeImpleteneted":"3"}
