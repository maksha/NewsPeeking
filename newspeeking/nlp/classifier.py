# newspeeking/nlp/classifier.py

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import Dict, List

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stop_words = set(stopwords.words('english'))


def classify_article(article_text: str, categories: Dict[str, List[str]]) -> str:
    tokens = word_tokenize(article_text.lower())
    filtered_tokens = [
        w for w in tokens if not w in stop_words and w.isalnum()]

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in filtered_tokens:
                return category
        return "General"
