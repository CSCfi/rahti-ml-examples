#!/usr/bin/env python3

import flask
import tempfile
from flask import send_file
from torch import autocast
from diffusers import StableDiffusionPipeline

application = flask.Flask(__name__)


@application.route('/text2image')
def text2image():
    prompt = flask.request.args.get("prompt", "a photo of an astronaut riding a horse on mars")

    # pipe = StableDiffusionPipeline.from_pretrained("/scratch/dac/stable-diffusion-v1-4")
    # 11G - 10458MB
    # git lfs install
    # git clone https://huggingface.co/CompVis/stable-diffusion-v1-4

    pipe = StableDiffusionPipeline.from_pretrained("/mountdata/stable-diffusion-v1-4")
    pipe = pipe.to("cuda")

    with autocast("cuda"):
        image = pipe(prompt).images[0]

    fp = tempfile.NamedTemporaryFile()
    image.save(fp.name)

    return send_file(fp.name, mimetype='image/png')


if __name__ == "__main__":
    application.run()
