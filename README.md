# Deploying BERT model for sentiment detection model using PyTorch

The [`onnx-imdb` branch](https://github.com/mvsjober/rahti-test/tree/onnx-imdb) of this repository contains an example of deploying a pre-trained BERT model for sentiment detection using PyTorch and the [Transformers library](https://huggingface.co/transformers/).  The pre-trained model has been saved in the [ONNX format in PyTorch](https://pytorch.org/docs/stable/onnx.html).

The branch has four files:
- [`onnx_imdb.py`](https://github.com/CSCfi/rahti-ml-examples/blob/onnx-imdb/onnx_imdb.py) contains the main code for predicting sentiments
- [`wsgi.py`](https://github.com/CSCfi/rahti-ml-examples/blob/onnx-imdb/wsgi.py) simply calls functions from the main code
- [`rahti_utils.py`](https://github.com/CSCfi/rahti-ml-examples/blob/onnx-imdb/rahti_utils.py) to download the pre-trained model file from [CSC's Allas object storage service](https://docs.csc.fi/#data/Allas/)
- [`requirements.txt`](https://github.com/CSCfi/rahti-ml-examples/blob/onnx-imdb/requirements.txt), which tells what Python packages Rahti should install when building the image.

## Setting up with Rahti

Setting up with Rahti is the same as with the [Minimal Python example](https://github.com/CSCfi/rahti-ml-examples#minimal-python-service-on-rahti), except that when giving the URL of the GitHub repository, you need to click "advanced options" and give the name of then branch in the "Git Reference" field (as it otherwise will default the main branch):

![Image of Rahti web user interface: configuration with advanced options](https://github.com/CSCfi/rahti-ml-examples/blob/master/images/rahti-advanced.png)

![Image of Rahti web user interface: configuration with Github branch](https://github.com/CSCfi/rahti-ml-examples/blob/master/images/rahti-advanced2.png)

After this Rahti will build your application and if everything goes well deploy it at something like http://appname-projectname.rahtiapp.fi . 

**Note**: inference with BERT is quite heavy, and you might need to add more cores to your pods and container in Rahti.
