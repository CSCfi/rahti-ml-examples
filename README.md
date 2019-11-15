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

- [wsgi.py](wsgi.py), which is the server script itself.  We are using [Flask](https://www.palletsprojects.com/p/flask/) which is a lightweight web application framework for Python.  As you can see from the code it's rather simple to set up different routes for the server to respond to.  Our example service responds with a simple JSON if you do a HTTP GET request to the root:

```bash
$ curl http://flask-mats-test.rahti-int-app.csc.fi/
{"msg":"Hello, World!"}
```

### Step 2: Create application in Rahti

- Head to <https://rahti.csc.fi/> and the link to the "Rahti web user interface", and log in with your CSC account.

- From the Service Catalog select "Python".

![Image of Rahti web user interface: selecting Python from the Service Catalog](images/rahti-1.png)

- In the next screen you will see some useful links, in particular the first tells about the [settings for the Python container image](https://github.com/sclorg/s2i-python-container/blob/master/3.6/README.md), which we can be useful for more advanced setups.  Just click next.

- In the next screen give your project and application some names, and point to your GitHub repository.

### Step 3: Wait and hope for the best :-)

After this Rahti will build your application and if everything goes well deploy it at something like `http://appname-projectname.rahtiapp.fi`.  If you have errors, take a look at the build log, and the pod log if the error appears only when the server is staring.  For more details see the [Rahti basic deployment documentation](https://rahti.csc.fi/tutorials/basic-console/).


## TensorFlow 2 example

<https://github.com/mvsjober/rahti-test/tree/tf2-imdb>


## PyTorch: BERT with ONNX

<https://github.com/mvsjober/rahti-test/tree/onnx-imdb>

## Turku neural parser pipeline

<https://github.com/mvsjober/Turku-neural-parser-pipeline>
