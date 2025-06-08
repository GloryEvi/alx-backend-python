#!/usr/bin/env python3

from typing import Dict, Tuple, Any, Callable
import requests
from functools import wraps


def access_nested_map(nested_map: Dict, path: Tuple[str]) -> Any:
    result = nested_map
    for key in path:
        try:
            result = result[key]
        except (KeyError, TypeError):
            raise KeyError(key)
    return result


def get_json(url: str) -> Dict:
    response = requests.get(url)
    return response.json()


def memoize(func: Callable) -> Callable:
    
    @wraps(func)
    def wrapper(self):
        attr_name = f"_{func.__name__}"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return wrapper