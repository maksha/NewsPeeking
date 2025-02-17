# newspeeking/crawler/crawler.py

from bs4 import BeautifulSoup
import requests
import validators
import time
import logging
from typing import List, Optional, Dict
# <--- Import urlparse from urllib.parse
from urllib.parse import urljoin, urlparse

from newspeeking.config import get_rate_limit_delay, get_categories, get_website_config, get_listing_page_config
from newspeeking.crawler.extractors import extract_article_data
from newspeeking.nlp.classifier import classify_article

logger = logging.getLogger(__name__)


def crawl_website(url: str, crawl_articles: bool = False) -> Optional[Dict | List[Dict]]:
    """
    Crawls a news website URL.
    If crawl_articles=False (default): Extracts and returns a list of article URLs from a listing page (if it's a listing page).
    If crawl_articles=True: Crawls individual articles from a listing page or a single article URL, extracts data, and classifies.
    """
    domain = urlparse(
        url).netloc  # <--- Use urllib.parse.urlparse instead of validators.urlparse
    # Get website-specific configurations
    website_config = get_website_config(domain)
    # Get website-specific rate limit delay
    rate_limit_delay = get_rate_limit_delay(domain)
    categories = get_categories()  # Categories are still default for now

    try:
        if not validators.url(url):
            raise ValueError("Invalid URL format")

        response = requests.get(
            url, headers={'User-Agent': 'NewsCrawlerAPI/1.0'})
        response.raise_for_status()
        time.sleep(rate_limit_delay)

        if not crawl_articles:  # Default mode: List article URLs from listing page
            article_urls = extract_article_urls_from_listing_page(
                url, website_config)
            return article_urls
        else:  # crawl_articles=True mode: Crawl and extract article data
            article_data = extract_article_data(
                url, response.text, website_config)
            # Check if article text was extracted
            if not article_data["article_text"]:
                logger.warning(f"No article text extracted from {url}")
                return None

            category = classify_article(
                article_data["article_text"], categories)
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


def extract_article_urls_from_listing_page(listing_url: str, website_config: Dict) -> List[str]:
    """
    Extracts article URLs from a news website listing page, using website-specific configurations.
    """
    article_urls = []
    try:
        if not validators.url(listing_url):
            raise ValueError("Invalid listing page URL format")

        response = requests.get(listing_url, headers={
                                'User-Agent': 'NewsCrawlerAPI/1.0'})
        response.raise_for_status()
        # <--- Corrected: Use urllib.parse.urlparse
        time.sleep(get_rate_limit_delay(urlparse(listing_url).netloc))

        soup = BeautifulSoup(response.text, 'html.parser')
        # Get listing page selectors from config
        listing_page_config = website_config.get('listing_page', {})

        # Default to all <a> tags if no selector in config
        article_link_selectors = listing_page_config.get(
            'article_link_selectors', ["a"])
        found_links = False
        for selector in article_link_selectors:
            article_link_tags = soup.select(selector)
            if article_link_tags:
                found_links = True
                for link_tag in article_link_tags:
                    href = link_tag.get('href')
                    if href:
                        absolute_url = urljoin(listing_url, href)
                        url_pattern_inclusion = listing_page_config.get(
                            'url_pattern_inclusion')
                        if url_pattern_inclusion:
                            # Handle single pattern string
                            if isinstance(url_pattern_inclusion, str):
                                if url_pattern_inclusion in absolute_url:
                                    article_urls.append(absolute_url)
                            # Handle list of pattern strings
                            elif isinstance(url_pattern_inclusion, list):
                                for pattern in url_pattern_inclusion:
                                    if pattern in absolute_url:
                                        article_urls.append(absolute_url)
                                        break  # Avoid adding the same URL multiple times if it matches multiple patterns

                if found_links:  # If links were found with a selector, stop using other selectors
                    break  # Move to the next selector if no links found

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for listing page URL {listing_url}: {e}")
    except ValueError as ve:
        logger.error(f"Listing page URL validation error: {ve}")
    except Exception as e:
        logger.error(
            f"Error extracting article URLs from listing page {listing_url}: {e}")

    return list(set(article_urls))
