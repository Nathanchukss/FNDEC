import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.preprocess import load_and_preprocess

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

CLASSIFIERS = {
    'logistic_regression': LogisticRegression(max_iter=1000, C=1.0),
    'passive_aggressive': PassiveAggressiveClassifier(max_iter=1000),
    'naive_bayes': MultinomialNB(),
}


def build_pipeline(classifier_name: str = 'logistic_regression') -> Pipeline:
    classifier = CLASSIFIERS.get(classifier_name)
    if classifier is None:
        raise ValueError(f"Unknown classifier: {classifier_name}. Choose from {list(CLASSIFIERS.keys())}")

    return Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )),
        ('clf', classifier),
    ])


def train(data_path: str, classifier_name: str = 'logistic_regression', test_size: float = 0.2):
    df = load_and_preprocess(data_path)

    X = df['processed']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    print(f"\nTraining with: {classifier_name}")
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    pipeline = build_pipeline(classifier_name)
    pipeline.fit(X_train, y_train)

    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, f'{classifier_name}.joblib')
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

    return pipeline, X_test, y_test
