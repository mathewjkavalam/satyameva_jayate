# AnimalList.py
animal_names = [
        "Lion", "Tiger", "Elephant", "Giraffe", "Zebra", "Kangaroo", "Panda", "Koala", "Penguin", "Ostrich"
    ]
from faker import Faker
import sqlite3
from datetime import datetime
from Python_Code.pages.AnimalList import animal_names  # Import the list of animal names
    
# Initialize Faker
fake = Faker()
    
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('animal_database.db')
cursor = conn.cursor()
    
# Create a table for storing animal names, sightings, images, and dates
cursor.execute('''
CREATE TABLE IF NOT EXISTS animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    image_url TEXT NOT NULL,
    sighting_date DATE NOT NULL
)
''')
    
# Define start and end timestamps
datetime_start = 946684800  # Unix timestamp for 2000-01-01 00:00:00
datetime_end = int(datetime.now().timestamp())  # Current Unix timestamp
    
 # Generate and insert fake animal sightings, images, and dates
for _ in range(5000):  # Adjust the range for the number of entries you want
    animal_name = fake.random_element(elements=animal_names)  # Select a random animal name from the list
    location = fake.city()
    image_url = fake.image_url()  # Generate a fake image URL
    sighting_date = fake.date_time_between_dates(datetime_start=datetime.fromtimestamp(datetime_start), datetime_end=datetime.fromtimestamp(datetime_end)).strftime('%Y-%m-%d %H:%M')  # Generate a random datetime between 2000 and now in 24-hour format with hour and minute
    cursor.execute('INSERT INTO animals (name, location, image_url, sighting_date) VALUES (?, ?, ?, ?)', (animal_name, location, image_url, sighting_date))
    
# Commit the transaction and close the connection
conn.commit()
conn.close()