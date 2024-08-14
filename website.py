import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('projects.db')
c = conn.cursor()

import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')

# Insert a record
c.execute("INSERT INTO users (name) VALUES ('Alice')")

# Commit the transaction
conn.commit()

# Fetch the data
c.execute('SELECT * FROM users')
print(c.fetchall())

# Close the connection
conn.close()


# Create a table to store project data if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gstin TEXT,
        pan TEXT,
        name TEXT,
        address TEXT
    )
''')

# Function to scrape project details
def scrape_project_details():
    url = 'https://hprera.nic.in/PublicDashboard'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    projects = []
    
    # Find the first 6 project rows in the "Registered Projects" section
    rows = soup.find_all('tr')[1:7]  # Adjust indexing based on the actual table structure

    for row in rows:
        cells = row.find_all('td')
        rera_number = cells[0].text.strip()
        name = cells[1].text.strip()
        address = cells[2].text.strip()
        
        # Assume the details are found by clicking on the RERA number link
        detail_link = cells[0].find('a')['href']
        detail_url = f'https://hprera.nic.in{detail_link}'
        detail_response = requests.get(detail_url, verify=False)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        gstin = detail_soup.find('span', {'id': 'GSTIN'}).text.strip()
        pan = detail_soup.find('span', {'id': 'PAN'}).text.strip()

        projects.append((gstin, pan, name, address))
        
    return projects

# Get project details and insert them into the database
projects = scrape_project_details()
c.executemany('INSERT INTO projects (gstin, pan, name, address) VALUES (?, ?, ?, ?)', projects)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data scraping and storing in SQL completed successfully.")
