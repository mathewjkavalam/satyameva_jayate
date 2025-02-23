import sqlite3
from typing import List, Tuple, Any, Optional

class Database:
    
    def __init__(self, db_name: str = "animal_database.db"):
        self.db_name = db_name

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def create_table(self, table_name: str, columns: List[Tuple[str, str]]):
        columns_str = ", ".join([f"{name} {dtype}" for name, dtype in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});"
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, table_name: str, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def fetch_all(self, table_name: str) -> List[Tuple[Any, ...]]:
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_by_condition(self, table_name: str, condition: str, values: Tuple) -> List[Tuple[Any, ...]]:
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def update(self, table_name: str, updates: dict, condition: str, values: Tuple):
        update_str = ", ".join([f"{key} = ?" for key in updates.keys()])
        query = f"UPDATE {table_name} SET {update_str} WHERE {condition}"
        self.cursor.execute(query, tuple(updates.values()) + values)
        self.connection.commit()

    def delete(self, table_name: str, condition: str, values: Tuple):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query, values)
        self.connection.commit()

    def fetch_one(self, table_name: str, condition: str, values: Tuple) -> Optional[Tuple[Any, ...]]:
        query = f"SELECT * FROM {table_name} WHERE {condition} LIMIT 1"
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

if __name__ == "__main__":
    with Database() as db:
        db.create_table("species_data", [
            ("id", "INTEGER PRIMARY KEY"),
            ("species", "TEXT"),
            ("image_path", "TEXT"),
            ("region", "TEXT"),
            ("date", "TEXT"),
            ("time", "REAL")
        ])
        
        species = input("Enter species: ")
        image_path = input("Enter image file path: ")
        region = input("Enter region: ")
        date = input("Enter date (YYYY-MM-DD): ")
        time = float(input("Enter time (Use . just after the hour to specify mins): "))
        
        db.insert("species_data",{
            "species": species,
            "image_path": image_path,
            "region": region,
            "date": date,
            "time": time
        })
        
        print("Data inserted successfully!")
        print(db.fetch_all("species_data"))