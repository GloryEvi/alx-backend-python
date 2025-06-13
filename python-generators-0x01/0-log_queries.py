import sqlite3
import functools

# decorator to log SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from either args or kwargs
        if args:
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']
        else:
            query = None
        
        if query:
            print(f"Executing SQL Query: {query}")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")