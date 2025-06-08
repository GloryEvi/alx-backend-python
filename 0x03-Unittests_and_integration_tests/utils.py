#!/usr/bin/env python3

from typing import Dict, Tuple, Any


def access_nested_map(nested_map: Dict, path: Tuple[str]) -> Any:
    result = nested_map
    for key in path:
        try:
            result = result[key]
        except (KeyError, TypeError):
            raise KeyError(key)
    return result