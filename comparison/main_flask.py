import logging
from flask import Flask, request, jsonify, Response

import comparison.constants as c
from comparison.fraud import LGBMFraudClassifier
from comparison.sentiment import TorchSentimentClassifier, message_bank
from comparison.schemas import (
    Transaction,
    Review,
)
from comparison.utils import setup_logging

setup_logging()
logger = logging.getLogger("api-comparison")

app = Flask(__name__)

logger.info("App set up")

fraud_classifier = LGBMFraudClassifier(c.DATA_DIR / "trained_lgbm_model.txt")
logger.info(f"{fraud_classifier=}")

sentiment_classifier = TorchSentimentClassifier()
logger.info(f"{sentiment_classifier=}")


@app.route("/fraud", methods=["POST"])
def predict_fraud() -> Response:
    logger.info("Received request:", request.json)
    if not isinstance(request.json, dict):
        raise ValueError("Invalid JSON data")
    transaction = Transaction(**request.json)
    is_fraud, probability = fraud_classifier.is_fraud(transaction)
    return jsonify({"is_fraud": is_fraud, "probability": probability})


@app.route("/sentiment", methods=["POST"])
def review_sentiment() -> Response:
    logger.info("Received request:", request.json)
    if not isinstance(request.json, dict):
        raise ValueError("Invalid JSON data")
    review = Review(**request.json)
    sentiment_score, sentiment = sentiment_classifier.get_sentiment(review.review)
    logger.info(f"Sentiment: {sentiment=}, {sentiment_score=}")
    return jsonify(
        {
            "sentiment_score": sentiment_score,
            "sentiment": sentiment.value,
            "message": message_bank[sentiment],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
