import pandas as pd
import pytest
from httpx import AsyncClient

import comparison.constants as c
from comparison.main_fastapi import app
from comparison.schemas import Transaction

@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"

@pytest.fixture(scope="session")
async def client() -> AsyncClient: #type: ignore
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def dummy_fraud_data() -> list[Transaction]:
    data = pd.read_csv(c.DATA_DIR / "dummy_fraud_data.csv")
    return [Transaction(**row) for _, row in data.iterrows()]

def transaction_to_dict(transaction: Transaction) -> dict:
    return {
        "transaction_amount": transaction.transaction_amount,
        "transaction_time": transaction.transaction_time.isoformat(),
        "new_device": transaction.new_device,
        "previous_purchases": transaction.previous_purchases,
        "user_logged_in": transaction.user_logged_in,
        "num_items_in_basket": transaction.num_items_in_basket,
        "min_basket_item_price": transaction.min_basket_item_price,
        "max_basket_item_price": transaction.max_basket_item_price,
    }

@pytest.mark.anyio
async def test_fraud(client: AsyncClient, dummy_fraud_data: list[Transaction]) -> None:
    for transaction in dummy_fraud_data:
        response = await client.post("/fraud", json=transaction_to_dict(transaction))
        assert response.status_code == 200
        is_fraud = response.json()["is_fraud"]
        probability = response.json()["probability"]
        assert type(is_fraud) == bool
        assert 0 <= probability <= 1

@pytest.mark.anyio
async def test_sentiment(client: AsyncClient) -> None:
    response = await client.post(
        "/sentiment",
        json={
            "text": "I love this product, it's amazing!",
        },
    )
    assert response.status_code == 200
    sentiment_score = response.json()["sentiment_score"]
    sentiment = response.json()["sentiment"]
    message = response.json()["message"]
    assert 0 <= sentiment_score <= 1
    assert sentiment in ["positive", "negative"]
    assert type(message) == str