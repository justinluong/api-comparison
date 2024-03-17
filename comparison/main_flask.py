import logging
from typing import Optional, Tuple, Protocol

from flask import Flask, request, jsonify, Response

import comparison.constants as c
from comparison.fraud import LGBMFraudClassifier
from comparison.sentiment import TorchSentimentClassifier
from comparison.schemas import (
    Transaction,
    Sentiment,
    SentimentResponse,
    FraudClassifier,
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
    print("Received request:", request.json)
    if not isinstance(request.json, dict):
        raise ValueError("Invalid JSON data")
    transaction = Transaction(**request.json)
    is_fraud, probability = fraud_classifier.is_fraud(transaction)
    return jsonify({"is_fraud": is_fraud, "probability": probability})

@app.route("/sentiment", methods=["POST"])
def review_sentiment() -> Response:
    print("Received request:", request.json)
    if not isinstance(request.json, dict):
        raise ValueError("Invalid JSON data")
    review = request.json.get("review")
    logger.info(review)

    logger.info(f"{sentiment_classifier=}")

    score, sentiment = sentiment_classifier.get_sentiment(review)
    return jsonify(SentimentResponse(score=score, sentiment=sentiment.value))


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
