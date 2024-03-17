from transformers import pipeline
import comparison.constants as c
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
