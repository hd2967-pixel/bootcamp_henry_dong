"""Flask API for the factor-model project.

Loads the trained model ONCE at startup and serves predictions for an asset's excess
return from four style-factor exposures (mkt_excess, size, value, momentum).

Routes:
    POST /predict                    body: {"features": [mkt, size, value, momentum]}
    GET  /predict/<mkt>/<size>/<value>/<momentum>
    GET  /run_full_analysis          returns the saved scenario-sensitivity metrics
"""

import json

import joblib
from flask import Flask, jsonify, request

# Loaded ONCE at startup — not inside a route.
model = joblib.load("model/model.pkl")
app = Flask(__name__)

FEATURES = ["mkt_excess", "size", "value", "momentum"]
N_FEATURES = len(FEATURES)


def _predict(vals):
    return float(model.predict([vals])[0])


@app.route("/predict", methods=["POST"])
def predict_post():
    data = request.get_json(silent=True) or {}
    features = data.get("features")

    if not isinstance(features, list) or len(features) != N_FEATURES:
        return jsonify({
            "error": "expected {'features': [mkt_excess, size, value, momentum]} "
                     "with exactly %d numbers" % N_FEATURES,
        }), 400

    try:
        pred = _predict(features)
    except (ValueError, TypeError):
        return jsonify({"error": "features must be numeric"}), 400

    return jsonify({"prediction": pred})


@app.route("/predict/<f1>/<f2>/<f3>/<f4>", methods=["GET"])
def predict_get(f1, f2, f3, f4):
    try:
        vals = [float(x) for x in (f1, f2, f3, f4)]
    except ValueError:
        return jsonify({"error": "path parameters must be numbers"}), 400

    return jsonify({"prediction": _predict(vals)})


@app.route("/run_full_analysis", methods=["GET"])
def run_full_analysis():
    """Return the saved scenario-sensitivity results as JSON."""
    try:
        with open("data/processed/scenario_results.json") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "scenario_results.json not found; run the pipeline first"}), 404


if __name__ == "__main__":
    # Port 5001 (not 5000): on macOS, port 5000 is often taken by AirPlay Receiver.
    app.run(host="127.0.0.1", port=5001)
