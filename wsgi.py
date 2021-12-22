#!/usr/bin/env python3

import flask
import torch
import transformers

application = flask.Flask(__name__)


@application.route('/')
def generate():
    default_text = "You didn't give me any input, so I'll just ramble on"
    text = flask.request.args.get("text", default_text)
    max_length = flask.request.args.get("max_length", 30)

    generator = transformers.pipeline('text-generation', model='gpt2')
    x = generator(text, max_length=max_length, num_return_sequences=1)

    return x[0]


@application.route('/versions')
def versions():
    return {
        'flask': flask.__version__,
        'torch': torch.__version__,
        'transformers': transformers.__version__,
    }


if __name__ == "__main__":
    application.run()
