from flask import Flask, request, jsonify
import joblib

# Loaded ONCE at startup — not inside a route.
# (A route that calls joblib.load on every request would re-read the file from
#  disk for every single caller, which is the mistake this task teaches us to avoid.)
model = joblib.load('model/model.pkl')
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict_post():
    data = request.get_json(silent=True) or {}
    features = data.get('features')

    if not isinstance(features, list) or len(features) != 2:
        return jsonify({'error': 'expected {"features": [f1, f2]} with exactly 2 numbers'}), 400

    try:
        pred = float(model.predict([features])[0])
    except (ValueError, TypeError):
        return jsonify({'error': 'features must be numeric'}), 400

    return jsonify({'prediction': pred})


@app.route('/predict/<f1>/<f2>', methods=['GET'])
def predict_get(f1, f2):
    # f1 and f2 arrive as STRINGS; convert to float and reject non-numbers.
    try:
        f1f, f2f = float(f1), float(f2)
    except ValueError:
        return jsonify({'error': 'path parameters must be numbers'}), 400

    pred = float(model.predict([[f1f, f2f]])[0])
    return jsonify({'prediction': pred})


if __name__ == '__main__':
    # Port 5001 (not 5000): on macOS, port 5000 is often taken by AirPlay Receiver.
    app.run(host='127.0.0.1', port=5001)
