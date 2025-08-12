# Python Generators — Streaming SQL Data

## 📌 Objective
Create a **generator** that streams rows from an SQL database **one by one** in a memory-efficient way.

---

## 🗄 Database Setup

### 1️⃣ Database & Table
- **Database:** `ALX_prodev`
- **Table:** `user_data`
- **Fields:**
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)

---

## ⚙️ Seed Script — `seed.py`

### Functions:
```python
def connect_db():
    """Connect to the MySQL database server"""

def create_database(connection):
    """Create ALX_prodev database if it does not exist"""

def connect_to_prodev():
    """Connect to ALX_prodev database"""

def create_table(connection):
    """Create user_data table with required fields"""

def insert_data(connection, data):
    """Insert data from CSV into database"""
