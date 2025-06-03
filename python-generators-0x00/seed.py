

#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    """
    Connects to the MySQL database server
    Returns connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='melisaglos2$'  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully or already exists")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    Returns connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='melisaglos2$',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist
    """
    try:
        cursor = connection.cursor()
        
        # Read CSV file and insert data
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Check if user_id already exists
                check_query = "SELECT COUNT(*) FROM user_data WHERE user_id = %s"
                cursor.execute(check_query, (row['user_id'],))
                count = cursor.fetchone()[0]
                
                # Insert only if user doesn't exist
                if count == 0:
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        row['user_id'],
                        row['name'],
                        row['email'],
                        int(row['age'])
                    ))
        
        connection.commit()
        print(f"Data from {csv_file} inserted successfully")
        cursor.close()
        
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Test the functions
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        
        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            connection.close()

