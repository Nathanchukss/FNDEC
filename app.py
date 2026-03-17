from flask import Flask, render_template, request, jsonify
from src.predict import predict

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def classify():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    if len(text) < 20:
        return jsonify({'error': 'Text too short. Please enter a full article or headline.'}), 400

    result = predict(text)
    return jsonify(result)


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
