from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import numpy as np

from sklearn import datasets
from sklearn.decomposition import PCA

import plotly.express as px
import plotly.graph_objects as go

iris = datasets.load_iris()
color = [iris['target_names'][t] for t in iris['target']]

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

@app.callback(
    Output("scatterplot", "figure"), 
    Input("vars", "value"))
def update_scatterplot(val):
    x, y = iris['data'][:,val], iris['data'][:,val+1]
    fig = px.scatter(x=x, y=y, color=color,
                     labels={"x": iris['feature_names'][val],
                             "y": iris['feature_names'][val+1]})
    return fig

pca_data = PCA(n_components=2).fit_transform(iris.data)
fig_pca = px.scatter(x=pca_data[:,0], y=pca_data[:,1], color=color,
                     labels={"x": "PCA dimension 1",
                             "y": "PCA dimension 2"})

app.layout = dbc.Container([ 
    html.H1(children='Dash Iris example'),

    html.H2(children='Scatterplot'),

    dbc.RadioItems(options=[{'label':'sepal', 'value':0},
                            {'label':'petal', 'value':2}],
                   value=0, id="vars"),
    
    dcc.Graph(id='scatterplot'),

    html.H2(children='PCA'),

    dcc.Graph(id='pca', figure=fig_pca),

])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
