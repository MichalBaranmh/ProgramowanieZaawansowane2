from typing import Optional

from fastapi import FastAPI, HTTPException,Query

from fastapi.middleware.cors import CORSMiddleware

from dbActions import init_db, db_writeRateFromRangeofDates,db_readCurrencyCode,db_readRates, db_readRatesFromQuarter, db_readRatesFromYear,db_readRatesFromRange

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
@app.get("/currencies")
def read_AvailableCurrencies():
    currencies = db_readCurrencyCode()
    return currencies

#wyswietlanie kursow z bazy danych 
@app.get("/currencies/getRates")
def read_AvailableCurrencies(
    year: Optional[int] = Query(None,description="Rok dla którego chcemy odczytać kursy"),
    quarter: Optional[int] = Query(None,description="Kwartał dla którego chcemy odczytać kursy"),
    month: Optional[int] = Query(None,description="Miesiąc dla którego chcemy odczytać kursy"),
    start_date: Optional[str] = Query(None,description="Data od której chcemy odczytać kursy"),
    end_date: Optional[str] = Query(None,description="Data do której chcemy odczytać kursy"),
    exact_date: Optional[str] = Query(None,description="Data dla której chcemy odczytać kursy")
):
    try:
        if exact_date:
            rates = db_readRates(exact_date)
        elif start_date and end_date:
            rates = db_readRatesFromRange(start_date,end_date)
        elif quarter:
            rates = db_readRatesFromQuarter(year,quarter)
        elif year:
            rates = db_readRatesFromYear(year)
        else:
            raise HTTPException(status_code=400,detail="Nie podano żadnych parametrów")
        
        return rates
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Nie udało się odczytać kursów: {e}")


#zdobywanie kursów z bazy danych Narodowego Banku Polskiego
@app.post("/currencies/fetch/{code}/{startDate}/{endDate}")
def write_FeedDatabase(code:str,startDate:str,endDate:str):
    codeUpper = code.upper()
    db_writeRateFromRangeofDates(codeUpper,startDate,endDate)
    


