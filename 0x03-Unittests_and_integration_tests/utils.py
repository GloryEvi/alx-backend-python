#!/usr/bin/env python3

from typing import Dict, Tuple, Any


def access_nested_map(nested_map: Dict, path: Tuple[str]) -> Any:
    """
    Access a nested map with a given path.
    
    Args:
        nested_map: A nested dictionary to access
        path: A tuple of keys representing the path to the desired value
        
    Returns:
        The value at the specified path in the nested dictionary
        
    Example:
        >>> access_nested_map({"a": 1}, ("a",))
        1
        >>> access_nested_map({"a": {"b": 2}}, ("a", "b"))
        2
    """
    result = nested_map
    for key in path:
        result = result[key]
    return result