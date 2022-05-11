# Deploying a Dash dashboard in Rahti

This branch  of this repository contains an example dashboard built using [Dash](https://plotly.com/dash/). The dashboard figures have been created with [Plotly](https://plotly.com/) and show the original variables and PCA of the [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris).

The branch has two files:
- [`app.py`](https://github.com/CSCfi/rahti-ml-examples/blob/dash/app.py) contains the code for the dashboard application.
- [`requirements.txt`](https://github.com/CSCfi/rahti-ml-examples/blob/dash/requirements.txt), which tells what Python packages Rahti should install when building the image.
  
## Setting up with Rahti

Setting up with Rahti is the same as with the [Minimal Python example](https://github.com/CSCfi/rahti-ml-examples#minimal-python-service-on-rahti), except that when giving the URL of the GitHub repository, you need to click "advanced options" and give the name of the branch (`dash` in this case) the "Git Reference" field (as it otherwise will default the main branch).

