from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

import comparison.constants as c
from comparison.sentiment import TorchSentimentClassifier

model = TorchSentimentClassifier()