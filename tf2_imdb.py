import json
import sys
from typing import Dict, Any

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub
from tensorflow.keras.models import load_model

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature

print('Using Tensorflow version: {}, and Keras version: {}.'.format(
    tf.__version__, tf.keras.__version__))
print(tf.config.get_visible_devices())

# create a distribution strategy
if tf.config.list_physical_devices('GPU'):
    strategy = tf.distribute.MirroredStrategy()
else:  # a default fallback strategy 
    strategy = tf.distribute.get_strategy()

print('Number of devices: {}'.format(strategy.num_replicas_in_sync))

class DetectSentiment:
    def __init__(self):
        # get the data
        self.train_data, self.validation_data, self.test_data = tfds.load(
            name="imdb_reviews",
            split=('train[:60%]', 'train[60%:]', 'test'),
            as_supervised=True)

        # build the model
        self.embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
        hub_layer = hub.KerasLayer(self.embedding, input_shape=[],
            dtype=tf.string, trainable=True)
        self.model = tf.keras.Sequential()
        self.model.add(hub_layer)
        self.model.add(tf.keras.layers.Dense(16, activation='relu'))
        self.model.add(tf.keras.layers.Dense(1))

    def predict(self, text: str, model_name: str):
        model = mlflow.pyfunc.load_model(
            model_uri=f"models:/{model_name}/Production"
        )

        pred = model.predict({"text": [text]})
 
        return pred.values.item(0)

    def train(self, model_name: str, hyperparams: Dict[str, Any],  epochs: int):
        #TODO: handle hyperparameters
        self.model.compile(optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy'])
        with strategy.scope():
            history = self.model.fit(self.train_data.shuffle(10000).batch(512),
                epochs=epochs, validation_data=self.validation_data.batch(512),
                verbose=0)

        df = tfds.as_dataframe(self.train_data.take(1), tfds.builder('imdb_reviews').info).drop('label', axis=1)
        sig = infer_signature(df, self.model.predict(df))

        return history, sig, df, self.model

if __name__ == '__main__':
    print('run the server as "python asgi.py"')