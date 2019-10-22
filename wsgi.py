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


@application.route('/versions')
def versions():
    return {
        'Flask': flask.__version__
    }


@application.route('/environ')
def environ():
    return dict(os.environ)


if __name__ == "__main__":
    application.run()
