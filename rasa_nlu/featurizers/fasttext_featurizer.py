from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Text

from rasa_nlu.featurizers import Featurizer
from rasa_nlu.components import Component
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData

import sys  

reload(sys)  
sys.setdefaultencoding('utf-8')

if typing.TYPE_CHECKING:
    import numpy as np

class FastTextFeaturizer(Featurizer):
    name = "intent_featurizer_fasttext"

    provides = ["text_features"]

    requires = ["fasttext_doc"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData) -> None

        fasttext = kwargs.get('fasttext')
        model = kwargs.get('model')
        for example in training_data.intent_examples:
            features = self.features_for_doc(example.get("fasttext_doc"), fasttext, model)
            example.set("text_features", self._combine_with_existing_text_features(example, features))

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None

        fasttext = kwargs.get('fasttext')
        model = kwargs.get('model')
        features = self.features_for_doc(message.get("fasttext_doc"), fasttext, model)
        message.set("text_features", self._combine_with_existing_text_features(message, features))

    def features_for_doc(self, doc, fasttext, model):
        # type: (Doc) -> np.ndarray

        from subprocess import Popen, PIPE, STDOUT
        import numpy as np

        cmd = '{} print-sentence-vectors {}'.format(fasttext, model)
        process = Popen(cmd.split(), stdout = PIPE, stdin = PIPE, stderr = STDOUT)
        x = process.communicate(input = doc)[0]
        return np.array(map(lambda x : float(x), x.split()[-300:]))
