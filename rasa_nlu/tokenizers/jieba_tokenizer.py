# -*- coding: utf-8 -*-
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
        jieba.suggest_freq('网站主', True)
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30]:
            jieba.suggest_freq(str(i) + u'天', True)
        for i in [1, 2, 3]:
            jieba.suggest_freq(str(i) + u'周', True)
            jieba.suggest_freq(str(i) + u'星期', True)
            jieba.suggest_freq(str(i) + u'个星期', True)
            jieba.suggest_freq(str(i) + u'月', True)
            jieba.suggest_freq(str(i) + u'个月', True)

        tokenized = list(jieba.tokenize(text))
        tokens = [Token(token, begin) for (token, begin, end) in tokenized]
        return tokens
