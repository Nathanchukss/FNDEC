import re
import ssl
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize_and_stem(text: str) -> str:
    tokens = word_tokenize(text)
    stemmed = [stemmer.stem(t) for t in tokens if t not in stop_words and len(t) > 2]
    return ' '.join(stemmed)


def preprocess(text: str) -> str:
    return tokenize_and_stem(clean_text(text))


def load_and_preprocess(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # Support common fake news dataset column schemas
    if 'text' not in df.columns:
        if 'title' in df.columns and 'author' in df.columns:
            df['text'] = df['title'].fillna('') + ' ' + df['author'].fillna('')
        elif 'title' in df.columns:
            df['text'] = df['title'].fillna('')

    df = df.dropna(subset=['text', 'label'])
    df['text'] = df['text'].astype(str)
    df['label'] = df['label'].astype(int)

    print(f"Loaded {len(df)} samples. Preprocessing...")
    df['processed'] = df['text'].apply(preprocess)
    print("Preprocessing complete.")
    return df
