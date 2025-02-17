# newspeeking/config.py

import yaml

_CONFIG_FILE_PATH = 'config.yaml'


def load_config():
    """Loads configuration from YAML file."""
    try:
        with open(_CONFIG_FILE_PATH, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found at: {_CONFIG_FILE_PATH}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration file: {e}")


_CONFIG = load_config()


def get_database_url():
    return _CONFIG.get('database_url')


def get_rate_limit_delay():
    return _CONFIG.get('rate_limit_delay', 1)


def get_categories():
    return _CONFIG.get('categories', {})
