#!/usr/bin/env python3

import flask
import os
import tempfile
import time
import torch
import transformers

from pathlib import Path


def load_gpt2():
    dummy = Path(os.path.join(tempfile.gettempdir(), "dummy"))

    # If dummy file exists, this means another process is currently downloading
    # the model file, so we wait
    while dummy.exists():
        print('[load_gpt2] Waiting for other process to download...')
        time.sleep(2)

    dummy.touch()
    ret = transformers.pipeline('text-generation', model='gpt2', device=0)
    os.remove(dummy)
    print('[load_gpt2] DONE')

    return ret


application = flask.Flask(__name__)
generator = load_gpt2()


@application.route('/')
def generate():
    default_text = "You didn't give me any input, so I'll just ramble on"
    text = flask.request.args.get("text", default_text)
    max_length = flask.request.args.get("max_length", 100, type=int)
    output = generator(text, max_length=max_length, num_return_sequences=1)

    return output[0]


@application.route('/versions')
def versions():
    return {
        'flask': flask.__version__,
        'torch': torch.__version__,
        'transformers': transformers.__version__,
    }


if __name__ == "__main__":
    application.run()
