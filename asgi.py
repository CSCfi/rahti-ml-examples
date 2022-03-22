#!/usr/bin/env python3
import numpy as np
import tensorflow as tf

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from urllib.parse import urlparse

import mlflow
from mlflow.tracking import MlflowClient

from tf2_imdb import DetectSentiment
from typing import Dict, Any

app = FastAPI()
ds = DetectSentiment()

mlflow.set_tracking_uri("sqlite:///db/backend.db")
mlflowclient = MlflowClient(mlflow.get_tracking_uri(), mlflow.get_registry_uri())

def train_task(model_name: str, hyperparams: Dict[str, Any],  epochs: int):
    """Trains and logs a model based on hyperparameters provided"""
    history, sig, eg, model = ds.train(model_name, hyperparams, epochs)
    # Set MLflow tracking
    mlflow.set_experiment("tf2_imdb")
    with mlflow.start_run() as run:
        print("Logging parameters and results")
        # Log parameters
        mlflow.log_params(hyperparams)

        # Log results
        for metric_name, metric_values in history.history.items():
            for metric_value in metric_values:
                mlflow.log_metric(metric_name, metric_value)

        # Log model
        mlflow.keras.log_model(model, model_name, 
            signature=sig, input_example=eg, 
            registered_model_name=model_name)                 
        
        # Take the last model version and tag it as production 
        mv = mlflowclient.search_model_versions(
            f"name='{model_name}'")[-1]  
        mlflowclient.transition_model_version_stage(
            name=mv.name, version=mv.version, stage="production")

@app.get("/models")
async def get_models():
    """Gets a list already trained model names"""
    model_list = mlflowclient.list_registered_models()
    model_list = [model.name for model in model_list]
    return model_list

@app.post("/train")
async def train(model_name:str, hyperparams:Dict[str, Any], epochs:int, bg_tasks: BackgroundTasks):    
    """Trains a sentiment classifier"""
    try:
        bg_tasks.add_task(train_task, model_name, hyperparams, epochs)
        return {"result": "Training task started. Check back in a moment to list trained models and use them for prediction"}
    except Exception as e:
        return {"result": f"Training failed to start: {e}"}

@app.post("/predict")
async def predict(text: str, model_name: str):
    """Predicts (classifies) the sentiment on the provided text"""
    try:
        p = ds.predict(text, model_name)
        return { 'text': text, 'sentiment': 'positive' if p > 0 else 'negative'}
    except Exception as e:
        return {'text': text,  'sentiment': e}

@app.post("/delete")
async def delete(model_name: str):
    """Deletes a model (all versions) if it exists"""
    try: 
        mlflowclient.delete_registered_model(name=model_name)
        return {"result": f"Deleted model: {model_name}"}
    except Exception as e:
        return {"result": f"Failed to delete model: {e}"}

@app.get('/versions')
async def versions():
    return {
        'NumPy': np.__version__,
        'TensorFlow': tf.__version__,
        'Keras': tf.keras.__version__,
        'Devices': tf.config.get_visible_devices()
    }

if __name__ == "__main__":
    uvicorn.run("asgi:app", host="0.0.0.0", port=8080, log_level="info")