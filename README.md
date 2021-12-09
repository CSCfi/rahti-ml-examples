# Deploying TensorFlow 2 sentiment detection model in Rahti

The [`tf2-imdb` branch](https://github.com/mvsjober/rahti-test/tree/tf2-imdb/) of this repository contains an example of deploying a pre-trained sentiment detection model using `tf.keras`. The model classifies movie reviews as positive or negative based on the IMDB dataset. 

The branch has four files:
- [`tf2_imdb.py`](https://github.com/mvsjober/rahti-test/blob/tf2-imdb/tf2_imdb.py) contains the main code for predicting sentiments of movie reviews
- [`wsgi.py`](https://github.com/mvsjober/rahti-test/blob/tf2-imdb/wsgi.py) simply calls functions from the main code
- [`rahti_utils.py`](https://github.com/mvsjober/rahti-test/blob/tf2-imdb/rahti_utils.py) to download the pre-trained model file from [CSC's Allas object storage service](https://docs.csc.fi/#data/Allas/)
- [`requirements.txt`](https://github.com/CSCfi/rahti-ml-examples/blob/tf2-imdb/requirements.txt), which tells what Python packages Rahti should install when building the image.

## Setting up with Rahti

Setting up with Rahti is the same as with the [Minimal Python example](https://github.com/CSCfi/rahti-ml-examples#minimal-python-service-on-rahti), except that when giving the URL of the GitHub repository, you need to click "advanced options" and give the name of then branch in the "Git Reference" field (as it otherwise will default the main branch):

![Image of Rahti web user interface: configuration with advanced options](https://github.com/CSCfi/rahti-ml-examples/blob/master/images/rahti-advanced.png)

![Image of Rahti web user interface: configuration with Github branch](https://github.com/CSCfi/rahti-ml-examples/blob/master/images/rahti-advanced2.png)

After this Rahti will build your application and if everything goes well deploy it at something like http://appname-projectname.rahtiapp.fi . As an output, you will get a sentiment prediction of a movie review. 