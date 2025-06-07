import sqlite3

class ExecuteQuery:
    """A context manager class to execute a query with parameters and return results"""
    
    def __init__(self, query, *params):
        #Initialize with the query and parameters
        self.query = query
        self.params = params
        self.connection = None
        self.results = None
    
    def __enter__(self):
        #Open the database connection and execute the query
        self.connection = sqlite3.connect('users.db')
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_value, traceback):
        #Close the database connection when exiting the context
        if self.connection:
            self.connection.close()
        # Return None (or False) to propagate any exceptions that occurred

# Using the ExecuteQuery context manager
with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as results:
    print("Query results:")
    for row in results:
        print(row)