from datetime import datetime
from enum import Enum
from typing import Optional, Protocol

from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_amount: float
    transaction_time: datetime
    new_device: bool
    previous_purchases: int
    user_logged_in: bool
    num_items_in_basket: int
    min_basket_item_price: Optional[float] = None
    max_basket_item_price: Optional[float] = None

class FraudPrediction(BaseModel):
    is_fraud: bool
    probability: Optional[float]

class Sentiment(str, Enum):
    positive = "positive"
    negative = "negative"

class SentimentResponse(BaseModel):
    sentiment_score: float
    sentiment: Sentiment
    message: str

class FraudClassifier(Protocol):
    def is_fraud(self, transaction: Transaction) -> tuple[bool, Optional[float]]: ...

class SentimentClassifier(Protocol):
    def get_sentiment(self, text: str) -> tuple[float, Sentiment]: ...
