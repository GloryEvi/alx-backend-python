

# import mysql.connector
# from mysql.connector import Error

# def stream_users():
#     """
#     Generator function that fetches rows one by one from the user_data table
#     Yields each row as a dictionary
#     Uses only one loop as required
#     """
#     connection = None
#     cursor = None
    
#     try:
#         # Connect to the ALX_prodev database
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root', 
#             password='melisaglos2$',  
#             database='ALX_prodev'
#         )
        
#         if connection.is_connected():
#             cursor = connection.cursor(dictionary=True)  # Use dictionary cursor
#             cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
#             # Single loop that yields rows one by one
#             for row in cursor:
#                 # Convert Decimal age to int for cleaner output
#                 if row['age']:
#                     row['age'] = int(row['age'])
#                 yield row
                
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
        
#     finally:
#         # Clean up resources
#         if cursor:
#             cursor.close()
#         if connection and connection.is_connected():
#             connection.close()



import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that fetches rows one by one from the user_data table
    Yields each row as a dictionary
    Uses only one loop as required
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='melisaglos2$', 
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Fetch all results first to avoid unread result error
            rows = cursor.fetchall()
            
            # Single loop that yields rows one by one
            for row in rows:
                # Convert Decimal age to int for cleaner output
                if row['age']:
                    row['age'] = int(row['age'])
                yield row
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()