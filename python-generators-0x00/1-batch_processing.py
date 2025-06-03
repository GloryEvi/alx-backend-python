#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table
    Yields batches of users as lists of dictionaries
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
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # LOOP 1: Fetch rows in batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                
                # Convert Decimal age to int for each user in batch
                processed_batch = []
                for user in batch:  # LOOP 2: Process each user in batch
                    if user['age']:
                        user['age'] = int(user['age'])
                    processed_batch.append(user)
                
                yield processed_batch
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    Prints each filtered user
    """
    # LOOP 3: Process each batch and filter users over 25
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
                print()  # Add empty line as shown in expected output