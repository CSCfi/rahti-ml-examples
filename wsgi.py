#!/usr/bin/env python3

from flask import Flask, escape, request
import gensim
import nltk

application = Flask(__name__)


@application.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@application.route('/versions')
def versions():
    import flask
    return """Flask version: {}
Gensim verison: {}
NLTK version: {}
""".format(flask.__version__,
           gensim.__version__,
           nltk.__version__)


if __name__ == "__main__":
    application.run()
