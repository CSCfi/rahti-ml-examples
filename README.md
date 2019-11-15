# Rahti machine learning deployment examples

This repository contains several simple examples of how to deploy machine learning inference jobs as a service on [CSC's Rahti](https://rahti.csc.fi/) container cloud.

If you are unfamiliar with Rahti and how to get access, first check [Rahti's documentation](https://rahti.csc.fi/).

The steps for running a service like this on Rahti go like this:

1. Set up a GitHub repository with your code, plus a few extra files needed by Rahti to run the code (more on this in the examples below).

2. Create a new Application in Rahti by selecting "Python" in the Service Catalog and pointing that to your GitHub repository.

3. Wait for Rahti to build your application and start it up... and (hopefully) enjoy your new service :-)

Next, we'll go through this in more detail, setting up a minimal Python web service.


## Minimal Python service on Rahti

### Step 1: GitHub repository

The `master` branch of this repository contains a minimal Python service that can be run on Rahti.  You can either use this repository directly, or make your own fork.  As you can see, we have two files: 

- [requirements.txt](requirements.txt), which says what Python packages Rahti should install when building the image.  In this minimal example we only use gunicorn and flask which are needed for setting up the web service itself.

- [wsgi.py](wsgi.py), which is the server script itself.  We are using [Flask](https://www.palletsprojects.com/p/flask/) which is a lightweight web application framework for Python.  As you can see from the code it's rather simple to set up different routes for the server to respond to.  Our example service responds with a simple "Hello, world" JSON if you do a HTTP GET request.

### Step 2: Create application in Rahti

- Head to <https://rahti.csc.fi/> and the link to the "Rahti web user interface", and log in with your CSC account.

- From the Service Catalog select "Python".

![Image of Rahti web user interface: selecting Python from the Service Catalog](images/rahti-1.png)

- In the next screen you will see some useful links, in particular the first tells about the [settings for the Python container image](https://github.com/sclorg/s2i-python-container/blob/master/3.6/README.md), which we can be useful for more advanced setups.  Just click next.

- In the next screen give your project and application some names, and point to your GitHub repository.

### Step 3: Wait and hope for the best :-)

After this Rahti will build your application and if everything goes well deploy it at something like `http://appname-projectname.rahtiapp.fi`.  Now you can try it out, for example from a unix shell:

```bash
$ curl http://appname-projectname.rahtiapp.fi/
{"msg":"Hello, World!"}
```

If you have errors, take a look at the build log, and the pod log if the error appears only when the server is staring.  For more details see the [Rahti basic deployment documentation](https://rahti.csc.fi/tutorials/basic-console/).

## TensorFlow 2 example

The [`tf2-imdb` branch](https://github.com/mvsjober/rahti-test/tree/tf2-imdb) of this repository contains an example of deploying a pre-trained sentiment detection model using `tf.keras`.

The main changes here is that the main code is in a separate file [`tf2_imdb.py`](https://github.com/mvsjober/rahti-test/blob/tf2-imdb/tf2_imdb.py), and `wsgi.py` simply calls functions from there.

The pre-trained model is downloaded from [CSC's Allas object storage service](https://docs.csc.fi/#data/Allas/).  This part requires some tricks as we start several processes in parallel to handle multiple HTTP requests, but we don't want them all to download the files.  The file downloading code can be found in [`rahti_utils.py`](https://github.com/mvsjober/rahti-test/blob/tf2-imdb/rahti_utils.py).

**NOTE:** Setting up with Rahti is the same as with the Minimal Python example, except that when giving the URL of the GitHub repository, you need to click "advanced options" and give the name of then branch in the "Git Reference" field (as it otherwise will default the master branch).

## PyTorch: BERT with ONNX

The [`onnx-imdb` branch](https://github.com/mvsjober/rahti-test/tree/onnx-imdb) of this repository contains an example of deploying a pre-trained BERT model for sentiment detection using PyTorch and the [Transformers library](https://huggingface.co/transformers/).  The pre-trained model has been saved in the [ONNX format in PyTorch](https://pytorch.org/docs/stable/onnx.html).

The main code can be found in [`onnx_imdb.py`](https://github.com/mvsjober/rahti-test/blob/onnx-imdb/onnx_imdb.py).

**NOTE:** Setting up with Rahti is the same as with the previous examples, but note that inference with BERT is quite heavy, and you might need to add more cores to your pods and container.


## Turku neural parser pipeline

Running the [Turku neural parser pipeline](http://turkunlp.org/Turku-neural-parser-pipeline/) in server mode on Rahti is pretty easy.  Just fork the [original GitHub repository](https://github.com/TurkuNLP/Turku-neural-parser-pipeline) and add a new file [`app.sh`](https://github.com/mvsjober/Turku-neural-parser-pipeline/blob/master/app.sh) containing the following lines:

```bash
#!/bin/bash
python3 fetch_models.py fi_tdt
python3 full_pipeline_server.py --gpu -1 --port 8080 --host 0.0.0.0 --conf models_fi_tdt/pipelines.yaml parse_plaintext
```

You also need to copy the file `requirements-cpu.txt` to `requirements.txt` so that Rahti can find it.  Here you can see an example of a working repository: <https://github.com/mvsjober/Turku-neural-parser-pipeline>.
