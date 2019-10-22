#!/usr/bin/env python3

import flask
import numpy
import tensorflow

from tf2_imdb import DetectSentiment

application = flask.Flask(__name__)
ds = DetectSentiment()


@application.route('/')
def predict():
    text = flask.request.args.get("text", "")
    p = ds.predict(text)
    print('Request for "{}" returned {}'.format(text, p))
    return {
        'text': text,
        'prediction': p,
        'sentiment': 'positive' if p > 0.5 else 'negative'
    }


@application.route('/versions')
def versions():
    return {
        'Flask': flask.__version__,
        'NumPy': numpy.__version__,
        'TensorFlow': tensorflow.__version__
    }


if __name__ == "__main__":
    application.run()
