import mysql.connector

# Connect to MySQL server (no specific database yet, just MySQL)
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Default MySQL username
    password="1234"  # Replace with your MySQL root password
)

# Create a cursor object to interact with MySQL
cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS web_scraping_db")

# Use the database
cursor.execute("USE web_scraping_db")

# Create the bulk_deals table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bulk_deals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    deal_date DATE,
    security_code VARCHAR(255),
    security_name VARCHAR(255),
    client_name VARCHAR(255),
    deal_type VARCHAR(255),
    quantity BIGINT,
    price DECIMAL(10, 2)
);
""")

# Create the commodity_prices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS commodity_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    industry VARCHAR(255),
    commodity_name VARCHAR(255),
    price DECIMAL(10, 2),
    date DATE
);
""")

print("Database and tables created successfully.")

# Close the connection
cursor.close()
conn.close()
