#!/usr/bin/env python3

from flask import Flask, escape, request
# import gensim
# import nltk
# import torch

application = Flask(__name__)

@application.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@application.route('/versions')
def versions():
    import flask
    return 'Flask version: {}\n'.format(flask.__version__)

if __name__ == "__main__":
    application.run()
