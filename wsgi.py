#!/usr/bin/env python3

import flask
import os

application = flask.Flask(__name__)


@application.route('/')
def hello():
    name = flask.request.args.get("name", "World")
    return {
        'msg': 'Hello, {}!'.format(flask.escape(name))
    }


if __name__ == "__main__":
    application.run()
