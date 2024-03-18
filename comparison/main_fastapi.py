from fastapi import FastAPI

import comparison.constants as c
from comparison.fraud import LGBMFraudClassifier
from comparison.sentiment import TorchSentimentClassifier, message_bank
from comparison.schemas import (
    FraudPrediction,
    Transaction,
    Review,
    SentimentResponse,
    FraudClassifier,
    SentimentClassifier,
)
from comparison.logging import setup_logging, get_logger

setup_logging()
logger = get_logger()

logger.info("Starting FastAPI app.")
app = FastAPI()

fraud_classifier: FraudClassifier = LGBMFraudClassifier(
    c.DATA_DIR / "trained_lgbm_model.txt"
)
logger.info(f"Succesfully loaded fraud classifier.")
sentiment_classifier: SentimentClassifier = TorchSentimentClassifier()
logger.info(f"Succesfully loaded sentiment classifier.")

@app.post("/fraud")
async def predict_fraud(transaction: Transaction) -> FraudPrediction:
    is_fraud, probability = fraud_classifier.is_fraud(transaction)
    return FraudPrediction(is_fraud=is_fraud, probability=probability)


@app.post("/sentiment")
async def review_sentiment(review: Review) -> SentimentResponse:
    logger.info(f"Received review: {review.review}")
    sentiment_score, sentiment = sentiment_classifier.get_sentiment(review.review)
    logger.info(f"Sentiment: {sentiment=}, {sentiment_score=}")
    return SentimentResponse(
        sentiment_score=sentiment_score,
        sentiment=sentiment,
        message=message_bank[sentiment],
    )
