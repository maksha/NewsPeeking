# newspeeking/crawler/extractors.py

from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def extract_article_data(url: str, html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')
    headline_tag = soup.find('h1') or soup.find('h2')
    headline = headline_tag.text.strip() if headline_tag else "Headline not found"

    article_tags = soup.find_all('p')
    article_text_parts = [tag.text.strip() for tag in article_tags]
    article_text = "\n".join(article_text_parts)

    publication_date = None
    date_tag = soup.find('time')
    if date_tag:
        try:
            publication_date_str = date_tag.get('datetime') or date_tag.text
            if publication_date_str:
                publication_date = datetime.fromisoformat(
                    publication_date_str.replace('Z', '+00:00'))
            else:
                publication_date = None
        except (ValueError, TypeError):
            logger.warning(f"Could not parse date from tag: {date_tag.text}")
            publication_date = None

    author = None
    author_tag = soup.find(attrs={'rel': 'author'}
                           ) or soup.find(class_='author')
    if author_tag:
        author = author_tag.text.strip()

    return {
        "headline": headline,
        "article_text": article_text,
        "publication_date": publication_date,
        "author": author
    }
