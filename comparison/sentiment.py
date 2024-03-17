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
        model_name: str = "roberta-base",
    ) -> None:
        self._config = RobertaConfig.from_pretrained(model_name)
        self._tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self._model = RobertaForSequenceClassification(
            config=self._config,
        )
        logger.info(f"{self._model=}")

    def get_sentiment(self, text: str) -> tuple[float, Sentiment]:
        logger.info(f"Received review: {text}")
        tokenized_text = self._tokenizer(text, return_tensors="pt")
        logger.info(f"{tokenized_text=}")
        result = self._model(**tokenized_text)
        logger.info(f"{result=}")
        score = 0.8
        label = "negative"
        sentiment = Sentiment[label]
        return score, sentiment
