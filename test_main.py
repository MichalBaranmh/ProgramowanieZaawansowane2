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

#test endpointu /currencies/{date}
def test_readCurrenciesByDate():
    date = "2024-01-01"
    response = client.get(f"/currencies/{date}")
    assert response.status_code == 200
    rates = response.json()
    assert isinstance(rates, list)
    for rate in rates:
        assert "RateId" in rate
        assert "code" in rate
        assert "effectiveDate" in rate
        assert "mid" in rate
        assert rate["effectiveDate"] == date


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