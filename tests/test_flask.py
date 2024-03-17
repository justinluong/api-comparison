import pandas as pd
import pytest

import comparison.constants as c
from comparison.main_flask import (
    app,
)  # Update this import according to your Flask app structure
from comparison.schemas import Transaction, Sentiment
from comparison.sentiment import message_bank


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def dummy_fraud_data() -> list[Transaction]:
    data = pd.read_csv(c.DATA_DIR / "dummy_fraud_data.csv")
    return [Transaction(**row.to_dict()) for _, row in data.iterrows()]


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


def test_fraud(client, dummy_fraud_data: list[Transaction]) -> None:
    for transaction in dummy_fraud_data:
        response = client.post("/fraud", json=transaction_to_dict(transaction))
        assert response.status_code == 200
        json_data = response.json
        assert isinstance(json_data["is_fraud"], bool)
        assert 0 <= json_data["probability"] <= 1
        break


def test_sentiment(client) -> None:
    test_cases: dict[str, Sentiment] = {
        "I love this product!": Sentiment.positive,
        "I hate this product!": Sentiment.negative,
    }

    for review, expected_sentiment in test_cases.items():
        response = client.post("/sentiment", json={"review": review})
        assert response.status_code == 200
        sentiment_score = response.json["sentiment_score"]
        sentiment = response.json["sentiment"]
        message = response.json["message"]
        assert type(sentiment_score) == float
        assert sentiment == expected_sentiment.value
        assert message == message_bank[expected_sentiment]
