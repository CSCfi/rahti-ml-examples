#!/usr/bin/env python3

from flask import Flask, escape, request
# import gensim
# import nltk
# import torch

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/versions')
def other():
    return f'Hello, other path'

if __name__ == "__main__":
    app.run()
else:
    print('\n * Server ready!')
