import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('WildlifeDatabasee.db')
cursor = conn.cursor()

# Drop the old table if it exists
cursor.execute('DROP TABLE IF EXISTS species_data;')

# Create the new species_data table without the image_path column
cursor.execute('''
CREATE TABLE IF NOT EXISTS species_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species TEXT NOT NULL,
    confidence REAL,
    region TEXT,
    date TEXT,
    time TEXT
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete. Table 'species_data' updated.")