import joblib
import os
from src.preprocess import preprocess

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')


def load_model(classifier_name: str = 'logistic_regression'):
    model_path = os.path.join(MODELS_DIR, f'{classifier_name}.joblib')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No trained model found at {model_path}. Run train first.")
    return joblib.load(model_path)


def predict(text: str, classifier_name: str = 'logistic_regression') -> dict:
    pipeline = load_model(classifier_name)
    processed = preprocess(text)
    prediction = pipeline.predict([processed])[0]
    proba = pipeline.predict_proba([processed])[0] if hasattr(pipeline.named_steps['clf'], 'predict_proba') else None

    result = {
        'label': 'FAKE' if prediction == 1 else 'REAL',
        'prediction': int(prediction),
    }
    if proba is not None:
        result['confidence'] = round(float(max(proba)), 4)

    return result
