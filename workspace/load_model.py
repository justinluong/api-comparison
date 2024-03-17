import cProfile
import pstats

from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

import comparison.constants as c
from comparison.sentiment import TorchSentimentClassifier

model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")