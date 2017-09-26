from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from typing import Any
from typing import List
from typing import Text

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.tokenizers import Token
from rasa_nlu.tokenizers import Tokenizer
from rasa_nlu.components import Component
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData


class JiebaTokenizer(Tokenizer, Component):
    name = 'tokenizer_jieba'

    provides = ['tokens']

    def __init__(self):
        pass

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ['jieba']

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None

        for example in training_data.training_examples:
            example.set('tokens', self.tokenize(example.text))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set('tokens', self.tokenize(message.text))

    @staticmethod
    def tokenize(text):
        # type: (Text) -> List[Token]

        import jieba

        tokenized = list(jieba.tokenize(text))
        tokens = [Token(token, begin) for (token, begin, end) in tokenized]
        return tokens
