# newspeeking/crawler/crawler.py

import requests
import validators
import time
import logging
from typing import Optional, Dict

from newspeeking.config import get_rate_limit_delay, get_categories
from newspeeking.crawler.extractors import extract_article_data
from newspeeking.nlp.classifier import classify_article

logger = logging.getLogger(__name__)
RATE_LIMIT_DELAY = get_rate_limit_delay()
CATEGORIES = get_categories()


def crawl_website(url: str) -> Optional[Dict]:
    try:
        if not validators.url(url):
            raise ValueError("Invalid URL format")

        response = requests.get(
            url, headers={'User-Agent': 'NewsCrawlerAPI/1.0'})
        response.raise_for_status()
        time.sleep(RATE_LIMIT_DELAY)

        article_data = extract_article_data(url, response.text)
        if not article_data["article_text"]:
            logger.warning(f"No article text extracted from {url}")
            return None

        category = classify_article(article_data["article_text"], CATEGORIES)
        article_data["category"] = category
        article_data["url"] = url

        return article_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for URL {url}: {e}")
        return None
    except ValueError as ve:
        logger.error(f"URL validation error: {ve}")
        return None
    except Exception as e:
        logger.error(f"Crawling error for URL {url}: {e}")
        return None
