import streamlit as st

import numpy as np

from sklearn import datasets
from sklearn.decomposition import PCA

import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

iris = datasets.load_iris()
color = [iris['target_names'][t] for t in iris['target']]

st.title('Streamlit Iris example')

st.header('Scatterplot')

selected = st.radio("Select variables to show:", ("sepal", "petal"))
val = 0 if selected == "sepal" else 2

x, y = iris['data'][:,val], iris['data'][:,val+1]
fig_sca = px.scatter(x=x, y=y, color=color,
                     labels={"x": iris['feature_names'][val],
                             "y": iris['feature_names'][val+1]})
st.plotly_chart(fig_sca, use_container_width=True)

st.header('PCA')

pca_data = PCA(n_components=2).fit_transform(iris.data)
fig_pca = px.scatter(x=pca_data[:,0], y=pca_data[:,1], color=color,
                     labels={"x": "PCA dimension 1",
                             "y": "PCA dimension 2"})
st.plotly_chart(fig_pca, use_container_width=True)
