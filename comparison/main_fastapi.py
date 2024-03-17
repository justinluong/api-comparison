import logging
from typing import Optional, Protocol

from fastapi import FastAPI

import comparison.constants as c
from comparison.fraud import LGBMFraudClassifier
from comparison.sentiment import TorchSentimentClassifier
from comparison.schemas import (
    FraudPrediction,
    Transaction,
    Sentiment,
    SentimentResponse,
    FraudClassifier,
    SentimentClassifier,
)
from comparison.utils import setup_logging, get_logger

setup_logging()
logger = get_logger()

app = FastAPI()

fraud_classifier: FraudClassifier = LGBMFraudClassifier(
    c.DATA_DIR / "trained_lgbm_model.txt"
)
logger.info(f"{fraud_classifier=}")

sentiment_classifier: SentimentClassifier = TorchSentimentClassifier()
logger.info(f"{sentiment_classifier=}")
# sentiment_classifier_gpu


@app.post("/fraud")
async def predict_fraud(transaction: Transaction) -> FraudPrediction:
    is_fraud, probability = fraud_classifier.is_fraud(transaction)
    return FraudPrediction(is_fraud=is_fraud, probability=probability)


@app.post("/sentiment")
async def review_sentiment(review: str) -> SentimentResponse:
    logger.info(f"Received review: {review}")
    sentiment_score, sentiment = sentiment_classifier.get_sentiment(review)
    logger.info(f"Sentiment: {sentiment=}, {sentiment_score=}")
    message_bank: dict[Sentiment, str] = {
        Sentiment.positive: "Thanks for the positive review! We appreciate you shopping with us.",
        Sentiment.negative: "We're sorry you didn't have a great experience, we will take on board your feedback.",
    }
    return SentimentResponse(
        sentiment_score=sentiment_score,
        sentiment=sentiment,
        message=message_bank[sentiment],
    )
