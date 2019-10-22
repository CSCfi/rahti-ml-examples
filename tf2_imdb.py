import json
import sys

import numpy as np
import tensorflow as tf

from rahti_utils import download_file
from tensorflow.keras.models import load_model

word_index_url = 'https://s3.amazonaws.com/text-datasets/imdb_word_index.json'
model_cnn1_url = 'https://a3s.fi/mldata/imdb-cnn1.h5'  # 88.88
oov_idx = 2  # out-of-vocabulary index

print('Using Tensorflow version: {}, and Keras version: {}.'.format(
    tf.__version__, tf.keras.__version__))


class DetectSentiment:
    def __init__(self):
        word_index_fname = download_file(word_index_url)
        self.word_index = json.load(open(word_index_fname))

        model_cnn1_name = download_file(model_cnn1_url)
        self.model = load_model(model_cnn1_name)

        self.embedding = self.model.get_layer(index=0)
        self.nb_words = self.embedding.input_dim
        self.maxlen = self.embedding.input_length

        print('Loaded model from', model_cnn1_url)
        # print(self.model.summary())

    def predict(self, text):
        v = np.zeros((1, self.maxlen), dtype=int)
        v[0, 0] = 1

        for i, w in enumerate(text.split()):
            idx = self.word_index[w] + 3 if w in self.word_index else oov_idx
            if idx >= self.nb_words:
                idx = oov_idx
            v[0, i+1] = idx

        p = self.model.predict(v, batch_size=1)
        return float(p[0, 0])


if __name__ == '__main__':
    ds = DetectSentiment()
    text = ' '.join(sys.argv[1:])
    print('Prediction for "{}": {}'.format(text, ds.predict(text)))
