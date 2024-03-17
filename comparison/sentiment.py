from pathlib import Path

import torch
from transformers import (
    RobertaTokenizer,
    RobertaForSequenceClassification,
    RobertaConfig,
    pipeline,
)

import comparison.constants as c
from comparison.schemas import Sentiment
from comparison.utils import get_logger

logger = get_logger()


class TorchSentimentClassifier:
    def __init__(
        self,
        model_path: Path = c.DATA_DIR / "pytorch_model.bin",
        model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest",
    ) -> None:
        self.pipeline = pipeline(
            "sentiment-analysis", model=model_name, tokenizer=model_name, device="mps"
        )
        logger.info(f"{self.pipeline=}")

    def get_sentiment(self, text: str) -> tuple[float, Sentiment]:
        result = self.pipeline(text)[0]
        score = result["score"]
        label = result["label"]
        sentiment = Sentiment[label]
        return score, sentiment
