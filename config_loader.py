# config_loader.py

import yaml
from pathlib import Path
from functools import lru_cache
from typing import Any, Dict

@lru_cache(maxsize=1)
def get_config(path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from a YAML file, cache on first read.
    
    Returns:
        A dict of nested configs, e.g. config['etrade']['consumer_key']
    Raises:
        FileNotFoundError: if the YAML file does not exist.
        yaml.YAMLError: on parse errors.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at: {config_path.resolve()}")
    with config_path.open("r") as f:
        data = yaml.safe_load(f)
    return data

# Example usage:
# from config_loader import get_config
# cfg = get_config()
# consumer_key = cfg["etrade"]["consumer_key"]
