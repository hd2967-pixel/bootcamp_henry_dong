# Stage 13 Homework — Prediction API

A trained `LinearRegression` model is served behind a Flask API. It takes two numeric features and returns
a single continuous prediction. This is a self-contained demo of taking a model out of a notebook and
putting it behind an endpoint that any other program can call.

## Running it

    python app.py

The server starts on **http://127.0.0.1:5001** and loads `model/model.pkl` once at startup.

> Note: port **5001** is used (not 5000) because on macOS port 5000 is often occupied by AirPlay Receiver.

## POST /predict

Send a JSON body with exactly two features:

    curl -X POST http://127.0.0.1:5001/predict \
         -H "Content-Type: application/json" \
         -d '{"features": [0.1, 0.2]}'

Response:

    {"prediction": 23.58961171297328}

## GET /predict/<f1>/<f2>

Pass the two features as path parameters:

    curl http://127.0.0.1:5001/predict/0.1/0.2

Response:

    {"prediction": 23.58961171297328}

## Bad input

Both routes return a JSON error with HTTP **400** (never a traceback):

- Missing `features` key or wrong number of features:

      curl -X POST http://127.0.0.1:5001/predict \
           -H "Content-Type: application/json" \
           -d '{"wrong_key": [0.1, 0.2]}'

  → `400 {"error": "expected {\"features\": [f1, f2]} with exactly 2 numbers"}`

- A path parameter that is not a number:

      curl http://127.0.0.1:5001/predict/abc/0.2

  → `400 {"error": "path parameters must be numbers"}`
