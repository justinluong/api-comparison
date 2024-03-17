from transformers import pipeline

from comparison.schemas import Sentiment
from comparison.utils import get_logger

logger = get_logger()

class TorchSentimentClassifier:
    def __init__(
        self,
        model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest",
    ) -> None:
        self._pipeline = pipeline("sentiment-analysis", model=model_name)

    def get_sentiment(self, text: str) -> tuple[float, Sentiment]:
        result = self._pipeline(text)
        return result[0]["score"], Sentiment(result[0]["label"])

message_bank: dict[Sentiment, str] = {
    Sentiment.positive: "Thanks for the positive review! We appreciate you shopping with us.",
    Sentiment.neutral: "We appreciate your feedback.",
    Sentiment.negative: "We're sorry you didn't have a great experience, we will take on board your feedback.",
}