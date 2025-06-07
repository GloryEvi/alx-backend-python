import time
import sqlite3 
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function and closes it afterward"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query parameter
        query = kwargs.get('query')
        
        # Check if result is already cached
        if query and query in query_cache:
            print(f"Cache hit! Returning cached result for query.")
            return query_cache[query]
        
        # Execute the function and cache the result if query exists
        result = func(*args, **kwargs)
        
        if query:
            print(f"Caching result for query.")
            query_cache[query] = result
        
        return result
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")