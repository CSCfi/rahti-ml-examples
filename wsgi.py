#!/usr/bin/env python3

import flask

from onnx_imdb import DetectSentiment

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


if __name__ == "__main__":
    application.run()
