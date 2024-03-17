from pathlib import Path
from typing import Any


import lightgbm as lgb
import numpy as np

from comparison.schemas import Transaction


class LGBMFraudClassifier:
    def __init__(self, model_path: str | Path, threshold: float = 0.5) -> None:
        self.model = lgb.Booster(model_file=model_path)
        self.threshold = threshold

    def _preprocess_transaction(
        self, transaction: Transaction
    ) -> np.ndarray[Any, Any]:
        return np.array(
            [
                transaction.transaction_amount,
                transaction.transaction_time.hour,
                transaction.new_device,
                transaction.previous_purchases,
                transaction.user_logged_in,
                transaction.num_items_in_basket,
                transaction.min_basket_item_price or 0,
                transaction.max_basket_item_price or 0,
            ]
        ).reshape(1, -1)

    def probability(self, transaction: Transaction) -> float:
        probability = self.model.predict(self._preprocess_transaction(transaction))
        probability = np.array(probability).item(0)
        return float(probability)

    def is_fraud(self, transaction: Transaction) -> tuple[bool, float]:
        probability = self.probability(transaction)
        return probability > self.threshold, probability
