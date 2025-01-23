'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

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

# Function to insert commodity data into MySQL
def insert_commodity_data(industry, data):
    query = """INSERT INTO commodity_prices (Industry, Date, Price, Unit)
               VALUES (%s, %s, %s, %s)"""
    cursor.executemany(query, data)
    db_connection.commit()

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape energy and steel data
def scrape_data():
    driver.get("https://www.sunsirs.com/CommodityPrice.html")
    time.sleep(5)

    # Navigate to the 'Energy' section
    energy_button = driver.find_element(By.LINK_TEXT, 'Energy')
    energy_button.click()
    time.sleep(3)

    # Scrape Energy data
    energy_table = driver.find_element(By.XPATH, "//table[@id='Energy']")
    energy_rows = energy_table.find_elements(By.TAG_NAME, "tr")
    energy_data = []
    for row in energy_rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        date = cols[0].text.strip()
        price = cols[1].text.strip()
        unit = cols[2].text.strip()
        energy_data.append(('Energy', date, price, unit))

    # Navigate to the 'Steel' section
    driver.back()
    steel_button = driver.find_element(By.LINK_TEXT, 'Steel')
    steel_button.click()
    time.sleep(3)

    # Scrape Steel data
    steel_table = driver.find_element(By.XPATH, "//table[@id='Steel']")
    steel_rows = steel_table.find_elements(By.TAG_NAME, "tr")
    steel_data = []
    for row in steel_rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        date = cols[0].text.strip()
        price = cols[1].text.strip()
        unit = cols[2].text.strip()
        steel_data.append(('Steel', date, price, unit))

    # Insert data into MySQL
    insert_commodity_data('Energy', energy_data)
    insert_commodity_data('Steel', steel_data)

# Call the function to scrape and insert data
scrape_data()

# Close the WebDriver and database connection
driver.quit()
db_connection.close()

print("Energy and Steel data scraped and inserted into MySQL successfully!")
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

# URL for SunSirs Commodity Prices
url = "https://www.sunsirs.com/CommodityPrice.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find Energy data
energy_link = soup.find('a', string="Energy")
energy_url = "https://www.sunsirs.com" + energy_link['href']
energy_response = requests.get(energy_url)
energy_soup = BeautifulSoup(energy_response.text, 'html.parser')

# Extract Energy data (adjust based on the table structure)
energy_table = energy_soup.find('table', {'class': 'table'})

# Scrape Energy commodity data
for row in energy_table.find_all('tr')[1:]:
    columns = row.find_all('td')
    commodity_name = columns[0].text.strip()
    price = float(columns[1].text.strip().replace(',', ''))
    date = columns[2].text.strip()

    # Insert into database
    insert_query = """
    INSERT INTO commodity_prices (industry, commodity_name, price, date) 
    VALUES (%s, %s, %s, %s)
    """
    data_to_insert = ('Energy', commodity_name, price, date)
    cursor.execute(insert_query, data_to_insert)

# Find Steel data
steel_link = soup.find('a', string="Steel")
steel_url = "https://www.sunsirs.com" + steel_link['href']
steel_response = requests.get(steel_url)
steel_soup = BeautifulSoup(steel_response.text, 'html.parser')

# Extract Steel data (adjust based on the table structure)
steel_table = steel_soup.find('table', {'class': 'table'})

# Scrape Steel commodity data
for row in steel_table.find_all('tr')[1:]:
    columns = row.find_all('td')
    commodity_name = columns[0].text.strip()
    price = float(columns[1].text.strip().replace(',', ''))
    date = columns[2].text.strip()

    # Insert into database
    insert_query = """
    INSERT INTO commodity_prices (industry, commodity_name, price, date) 
    VALUES (%s, %s, %s, %s)
    """
    data_to_insert = ('Steel', commodity_name, price, date)
    cursor.execute(insert_query, data_to_insert)

# Commit the transaction
conn.commit()
print("Data inserted successfully into commodity_prices.")

# Close the connection
cursor.close()
conn.close()

