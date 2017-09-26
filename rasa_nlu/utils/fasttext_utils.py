from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Text

from rasa_nlu.components import Component
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from rasa_nlu.model import Metadata


class FastTextNLP(Component):
    name = "nlp_fasttext"

    provides = ["fasttext_doc"]

    def __init__(self, language, fasttext_model_name, fasttext, model):
        # type: (Text, Text) -> None
        self.language = language
        self.fasttext_model_name = fasttext_model_name
        self.fasttext = fasttext
        self.model = model

    @classmethod
    def create(cls, config):
        # type: (RasaNLUConfig) -> FastTextNLP

        language = config["language"]
        if language != 'zh':
            raise Exception("fasttext_nlp is only used for Chinese. Check your config file.")
        fasttext_model_name = config["fasttext_model_name"]
        if fasttext_model_name == None:
            fasttext_model_name = language
        logger.info("Trying to load fasttext model with name '{}'".format(fasttext_model_name))
        fasttext = config['fasttext']
        model = config['model']
        return FastTextNLP(language, fasttext_model_name, fasttext, model)

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> Text

        fasttext_model_name = model_metadata.metadata.get("fasttext_model_name")
        if fasttext_model_name is None:
            # Fallback, use the language name, e.g. "zh", as the model name if no explicit name is defined
            fasttext_model_name = model_metadata.language
        return cls.name + "-" + fasttext_model_name

    def provide_context(self):
        # type: () -> Dict[Text, Any]

        return {'fasttext' : self.fasttext, 'model' : self.model}

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData) -> Dict[Text, Any]

        for example in training_data.training_examples:
            example.set("fasttext_doc", example.text)

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        message.set("fasttext_doc", message.text)

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]

        return {
            "fasttext_model_name": self.fasttext_model_name,
            "language": self.language,
            "fasttext": self.fasttext,
            "model": self.model
        }

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[FastTextNLP], **Any) -> FastTextNLP

        if cached_component:
            return cached_component

        return FastTextNLP(model_metadata.get("language"), model_metadata.get("fasttext_model_name"),
                           model_metadata.get("fasttext"), model_metadata.get("model"))
