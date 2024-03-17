import random

import pandas as pd
from locust import HttpUser, task, constant

import comparison.constants as c
from comparison.schemas import Transaction


def dummy_fraud_data() -> list[Transaction]:
    data = pd.read_csv(c.DATA_DIR / "dummy_fraud_data.csv")
    return [Transaction(**row) for _, row in data.iterrows()]

transactions = dummy_fraud_data()

reviews: list[str] = [
    "I love this product!",
    "I hate this product!",
]

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


class User(HttpUser):
    wait_time = constant(0)

    @task
    def fraud(self) -> None:
        transaction = random.choice(transactions)
        request_payload = transaction_to_dict(transaction)
        self.client.post(
            "/fraud",
            json=request_payload,
            name="Fraud",
        )

    @task
    def sentiment(self) -> None:
        review = random.choice(reviews)
        self.client.post(
            "/sentiment",
            json={"review": review},
            name="Sentiment",
        )