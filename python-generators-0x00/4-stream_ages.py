#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database
    Memory-efficient approach - processes one age at a time
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
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data")
            
            # LOOP 1: Yield ages one by one
            for (age,) in cursor:
                # Convert Decimal to int and yield
                yield int(age) if age else 0
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def calculate_average_age():
    """
    Calculate average age using the generator without loading entire dataset into memory
    Uses streaming approach to maintain constant memory usage
    """
    total_age = 0
    count = 0
    
    # LOOP 2: Process ages one by one using generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found in database")

if __name__ == "__main__":
    calculate_average_age()