import sqlite3

class DatabaseConnection:
    """A context manager class to handle opening and closing database connections automatically"""
    
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
    
    def __enter__(self):
        #open
        self.connection = sqlite3.connect(self.database_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        #close
        if self.connection:
            self.connection.close()
        # Return None (or False) to propagate any exceptions that occurred


with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query results:")
    for row in results:
        print(row)