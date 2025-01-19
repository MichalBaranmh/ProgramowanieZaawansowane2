import pytest
from fastapi.testclient import TestClient
from main import app

from dbActions import CurrencyCode,Rate,Transaction, init_db, engine
from sqlmodel import SQLModel,Session,select


client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield

#test enpointu /currencies
def test_readCurrencies():
    response = client.get("/currencies")
    assert response.status_code == 200

#test endpointu /currencies/GetRates
def test_readCurrenciesByDate():
    date = "2024-01-01"
    response = client.get(f"/currencies/getRates?exact_date={date}")
    assert response.status_code == 200
    rates = response.json()
    assert isinstance(rates, list)
    for rate in rates:
        assert "RateId" in rate
        assert "code" in rate
        assert "effectiveDate" in rate
        assert "mid" in rate
        assert rate["effectiveDate"] == date



#test endpointu /currencies/GetRates range
def test_readCurrenciesByRange():
    start_date = "2024-01-01"
    end_date = "2024-01-07"
    response = client.get(f"/currencies/getRates?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    rates = response.json()
    assert isinstance(rates, list)
    for rate in rates:
        assert "RateId" in rate
        assert "code" in rate
        assert "effectiveDate" in rate
        assert "mid" in rate
        assert rate["effectiveDate"] >= start_date
        assert rate["effectiveDate"] <= end_date

#test endpointu /currencies/GetRates quarter
def test_readCurrenciesByQuarter():
    year = 2024
    quarter = 1
    response = client.get(f"/currencies/getRates?year={year}&quarter={quarter}")
    assert response.status_code == 200
    rates = response.json()
    assert isinstance(rates, list)
    for rate in rates:
        assert "RateId" in rate
        assert "code" in rate
        assert "effectiveDate" in rate
        assert "mid" in rate
        assert rate["effectiveDate"] >= f"{year}-01-01"
        assert rate["effectiveDate"] <= f"{year}-03-31"

#test endpointu /currencies/GetRates year
def test_readCurrenciesByYear():
    year = 2024
    response = client.get(f"/currencies/getRates?year={year}")
    assert response.status_code == 200
    rates = response.json()
    assert isinstance(rates, list)
    for rate in rates:
        assert "RateId" in rate
        assert "code" in rate
        assert "effectiveDate" in rate
        assert "mid" in rate
        assert rate["effectiveDate"] >= f"{year}-01-01"
        assert rate["effectiveDate"] <= f"{year}-12-31"


#test endpointu post /currencies/fetch/{code}/{startDate}/{endDate}
def test_writeFeedDatabaseOK():
    code = "USD"
    start_date = "2024-01-01"
    end_date = "2024-01-07"
    response = client.post(f"/currencies/fetch/{code}/{start_date}/{end_date}")
    assert response.status_code == 200

#brak kodu waluty
def test_writeFeedDatabaseWithWrongCode():
    code = "DSU"
    start_date = "2024-01-01"
    end_date = "2024-01-07"
    response = client.post(f"/currencies/fetch/{code}/{start_date}/{end_date}")
    assert response.status_code == 404