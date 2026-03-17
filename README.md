# FNDEC — Fake News Detection Classifier

**Live Demo:** https://fndec.onrender.com (hosted on Render)

An NLP-based classification model that identifies fake news by preprocessing 10,000+ text samples through tokenization, stemming, and TF-IDF vectorization.

---

## Features

- Text cleaning: lowercasing, URL removal, punctuation stripping
- NLP preprocessing: tokenization, stopword removal, Porter stemming
- TF-IDF vectorization with bigram support (up to 10,000 features)
- Three classifier options: Logistic Regression, Passive-Aggressive, Naive Bayes
- Evaluation with accuracy, classification report, and confusion matrix
- CLI interface for training and inference

---

## Project Structure

```
FNDEC/
├── data/               # Place your dataset CSV here
├── models/             # Saved trained models
├── src/
│   ├── preprocess.py   # Text cleaning, tokenization, stemming
│   ├── train.py        # TF-IDF + classifier pipeline, model saving
│   ├── evaluate.py     # Metrics and confusion matrix
│   └── predict.py      # Inference on new text
├── main.py             # CLI entry point
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Dataset

This project is compatible with the [Kaggle Fake News Dataset](https://www.kaggle.com/c/fake-news/data).

Download and place `train.csv` in the `data/` folder. The dataset should have:
- `text` (or `title` + `author`) column
- `label` column: `0` = Real, `1` = Fake

---

## Usage

### Train
```bash
python main.py train --data data/train.csv --model logistic_regression
```

Available models: `logistic_regression`, `passive_aggressive`, `naive_bayes`

### Predict
```bash
python main.py predict --text "Scientists discover cure for all diseases overnight"
```

---

## Results (Logistic Regression on Kaggle Fake News Dataset)

| Metric    | Score  |
|-----------|--------|
| Accuracy  | ~98%   |
| Precision | ~98%   |
| Recall    | ~98%   |
| F1 Score  | ~98%   |

---

## Tech Stack

- **Language:** Python 3.10+
- **NLP:** NLTK (tokenization, stemming, stopwords)
- **ML:** scikit-learn (TF-IDF, Logistic Regression, Passive-Aggressive, Naive Bayes)
- **Data:** pandas, numpy
- **Visualization:** matplotlib, seaborn
