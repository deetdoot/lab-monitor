import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',         # Change as needed
    'password': '1234',         # Change as needed
}

# Connect to MySQL server
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS `lab-monitor`")
cursor.execute("USE `lab-monitor`")

# Create table
create_table_query = """
CREATE TABLE IF NOT EXISTS `PrimaryTable` (
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Track_ID VARCHAR(255) NOT NULL,
    Duration INT
)
"""
cursor.execute(create_table_query)

print("Database and table created successfully.")

cursor.close()
conn.close()
