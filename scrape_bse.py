'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import mysql.connector
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: run in headless mode

# Path to ChromeDriver
driver_path = r'path_to_chromedriver'  # Update this path

# Set up MySQL connection
db_connection = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_database_name"
)
cursor = db_connection.cursor()

# Function to insert data into MySQL
def insert_bulk_deals(data):
    query = """INSERT INTO bulk_deals (Date, Company, Quantity, Price, Value) 
               VALUES (%s, %s, %s, %s, %s)"""
    cursor.executemany(query, data)
    db_connection.commit()

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the BSE website
driver.get("https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx")

# Wait for the page to load
time.sleep(5)

# Locate the table
table = driver.find_element(By.ID, "ContentPlaceHolder1_grdBulkDeal")

# Extract data from the table
rows = table.find_elements(By.TAG_NAME, "tr")
bulk_deals = []

for row in rows[1:]:
    cols = row.find_elements(By.TAG_NAME, "td")
    date = cols[0].text.strip()
    company = cols[1].text.strip()
    quantity = cols[2].text.strip()
    price = cols[3].text.strip()
    value = cols[4].text.strip()
    bulk_deals.append((date, company, quantity, price, value))

# Insert data into MySQL
insert_bulk_deals(bulk_deals)

# Close the WebDriver and database connection
driver.quit()
db_connection.close()

print("Data scraped and inserted into MySQL successfully!")
'''

import mysql.connector
import requests
from bs4 import BeautifulSoup

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="web_scraping_db"
)

cursor = conn.cursor()

# URL for BSE Bulk Deals
url = "https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table (adjust the selector based on the actual page structure)
table = soup.find('table', {'id': 'ContentPlaceHolder1_grdBulkDeal'})
rows = table.find_all('tr')[1:]  # Skip header row

# Loop through the rows and extract data
for row in rows:
    columns = row.find_all('td')
    deal_date = columns[0].text.strip()
    security_code = columns[1].text.strip()
    security_name = columns[2].text.strip()
    client_name = columns[3].text.strip()
    deal_type = columns[4].text.strip()
    quantity = int(columns[5].text.strip().replace(',', ''))
    price = float(columns[6].text.strip().replace(',', ''))

    # Insert data into the database
    insert_query = """
    INSERT INTO bulk_deals (deal_date, security_code, security_name, client_name, deal_type, quantity, price) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data_to_insert = (deal_date, security_code, security_name, client_name, deal_type, quantity, price)
    cursor.execute(insert_query, data_to_insert)

# Commit the transaction
conn.commit()
print("Data inserted successfully into bulk_deals.")

# Close the connection
cursor.close()
conn.close()
