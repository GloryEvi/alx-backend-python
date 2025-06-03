#!/usr/bin/python3

import seed

def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the database
    Args:
        page_size: Number of users per page
        offset: Starting position (0-based)
    Returns:
        List of user dictionaries
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    
    # Convert Decimal age to int for cleaner output
    for row in rows:
        if row['age']:
            row['age'] = int(row['age'])
    
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator function that lazily loads pages of users
    Only fetches the next page when needed
    Uses only one loop as required
    
    Args:
        page_size: Number of users per page
    
    Yields:
        List of users for each page
    """
    offset = 0
    
    # Single loop that continues until no more data
    while True:
        # Fetch the current page
        page_data = paginate_users(page_size, offset)
        
        # If no data returned, we've reached the end
        if not page_data:
            break
            
        # Yield the current page
        yield page_data
        
        # Move to next page
        offset += page_size

# Alias for the function name used in the test script
lazy_pagination = lazy_paginate