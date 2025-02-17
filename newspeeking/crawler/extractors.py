# newspeeking/crawler/extractors.py

from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


def extract_article_data(url: str, html_content: str, website_config: Dict) -> Dict:
    """
    Extracts headline, article text, publication date, and author from HTML content,
    using website-specific configurations.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Get article page selectors from config
    article_page_config = website_config.get('article_page', {})

    # --- Headline Extraction ---
    headline_selector = article_page_config.get('headline_selector')
    headline_tag = soup.select_one(headline_selector) if headline_selector else soup.find(
        'h1') or soup.find('h2')  # Fallback to h1 or h2 if no selector
    headline = headline_tag.text.strip() if headline_tag else "Headline not found"

    # --- Article Text Extraction ---
    article_text_selector = article_page_config.get('article_text_selector')
    article_tags = soup.select(article_text_selector) if article_text_selector else soup.find_all(
        'p')  # Fallback to <p> tags
    article_text_parts = [tag.text.strip() for tag in article_tags]
    article_text = "\n".join(article_text_parts)

    # --- Publication Date Extraction ---
    publication_date_selector = article_page_config.get(
        'publication_date_selector')
    date_tag = soup.select_one(publication_date_selector) if publication_date_selector else soup.find(
        'time')  # Fallback to <time> tag
    publication_date = None
    if date_tag:
        try:
            publication_date_str = date_tag.get(
                'datetime') or date_tag.text  # Try datetime attribute or text
            if publication_date_str:
                publication_date = datetime.fromisoformat(
                    # Handle ISO format
                    publication_date_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            logger.warning(
                f"Could not parse date from tag: {date_tag.text}")

    # --- Author Extraction ---
    author_selector = article_page_config.get('author_selector')
    author_tag = soup.select_one(author_selector) if author_selector else soup.find(
        # Fallback to rel='author' or class='author'
        attrs={'rel': 'author'}) or soup.find(class_='author')
    author = author_tag.text.strip() if author_tag else None

    return {
        "headline": headline,
        "article_text": article_text,
        "publication_date": publication_date if publication_date else None,
        "author": author
    }
