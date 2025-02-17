# newspeeking/config.py

import yaml
import logging

_CONFIG_FILE_PATH = 'config.yaml'
_CONFIG = None  # Initialize _CONFIG to None
logger = logging.getLogger(__name__)


def load_config():
    """Loads configuration from YAML file and caches it."""
    global _CONFIG  # Use the global _CONFIG variable
    if _CONFIG is None:  # Load config only once
        try:
            with open(_CONFIG_FILE_PATH, 'r') as f:
                _CONFIG = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(
                f"Configuration file not found at: {_CONFIG_FILE_PATH}")
            raise FileNotFoundError(
                f"Configuration file not found at: {_CONFIG_FILE_PATH}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration file: {e}")
            raise ValueError(f"Error parsing YAML configuration file: {e}")
        except Exception as e:  # Catch any other potential exception
            logger.error(f"Unexpected error during config loading: {e}")
            # Raise RuntimeError
            raise RuntimeError(
                f"Failed to load configuration due to an unexpected error: {e}")
    return _CONFIG


def get_default_config():
    """Returns the default configuration settings."""
    config = load_config()
    return config.get('default', {})


def get_website_config(domain: str):
    """
    Returns website-specific configuration settings for a given domain.
    Returns an empty dictionary if no configuration is found for the domain.
    """
    config = load_config()
    return config.get('websites', {}).get(domain, {})


def get_rate_limit_delay(domain: str = None):
    """Returns the rate limit delay, website-specific if available, otherwise default."""
    website_cfg = get_website_config(domain) if domain else {}
    default_config = get_default_config()  # Get default config
    # Use default_config for fallback
    return website_cfg.get('rate_limit_delay', default_config.get('rate_limit_delay', 1))


def get_categories():
    """Returns the categories configuration (default)."""
    default_config = get_default_config()  # Get default config
    return default_config.get('categories', {})  # Get from default_config


def get_listing_page_config(domain: str):
    """Returns the listing page configuration for a given domain."""
    website_cfg = get_website_config(domain)
    return website_cfg.get('listing_page', {})


def get_article_page_config(domain: str):
    """Returns the article page configuration for a given domain."""
    website_cfg = get_website_config(domain)
    return website_cfg.get('article_page', {})


def get_database_url():
    """Returns the database URL from configuration."""
    default_config = get_default_config()  # Get default config
    return default_config.get('database_url')  # Get from default_config
