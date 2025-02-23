import sqlite3
import threading

class Database:
    def __init__(self, db_name="WildlifeNew.db"):
        """
        Initialize the database connection.
        """
        self.db_name = db_name
        self.local = threading.local()
        self._create_table()  # Ensure table exists on initialization
        print(f"✅ Initialized database: {self.db_name}")

    def get_connection(self):
        """
        Get a thread-local SQLite connection.
        """
        if not hasattr(self.local, "connection"):
            print(f"🔄 Creating new connection to database: {self.db_name}")
            self.local.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.local.cursor = self.local.connection.cursor()
        return self.local.connection, self.local.cursor

    def _create_table(self):
        """
        Create the 'species_data' table if it doesn't exist.
        """
        conn, cursor = self.get_connection()
        print("📊 Creating table 'species_data' if it doesn't exist...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS species_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                species TEXT,
                confidence REAL,
                region TEXT,
                date TEXT,
                time TEXT,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()
        print("✅ Table 'species_data' created successfully.")

    def insert_data(self, species, confidence, region, date, time, latitude, longitude):
        """
        Insert a new observation into the database.
        """
        conn, cursor = self.get_connection()
        print(f"📥 Inserting data: {species}, {confidence}, {region}, {date}, {time}, {latitude}, {longitude}")
        query = """
            INSERT INTO species_data (species, confidence, region, date, time, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (species, confidence, region, date, time, latitude, longitude))
        conn.commit()
        print("✅ Data inserted successfully.")
