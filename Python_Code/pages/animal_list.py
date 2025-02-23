import streamlit as st
from collections import defaultdict
import sqlite3
import os


st.set_page_config(page_title="Animal List from A-Z", layout="wide")

# Define the database path
db_path = os.path.join(os.path.dirname(__file__), '..', 'WildlifeNew.db')

# Function to fetch animal list from the new database
def fetch_animals_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM species")
    animals_data = cursor.fetchall()
    conn.close()
    return animals_data

# Fetch animals
animals_data = fetch_animals_from_db()
animals = [animal[0] for animal in animals_data]

# Function to fetch animal information from the new database
def fetch_animal_info(animal_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT info FROM animal_info WHERE name=?", (animal_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Information not available."

# Categorize animals by their starting alphabet
animal_dict = defaultdict(list)
for animal in animals:
    animal_dict[animal[0]].append(animal)

# Streamlit app
st.title("Animal List from A-Z")

# Add a search bar
search_query = st.text_input("Search for an animal:")

# Add some styling
st.markdown("""
    <style>
    .stExpander {
        background-color: #242526;
        border: 3px solid #ddd;
        border-radius: 25px;
        padding: 10px;
        margin-bottom: 10px;
        width: 45%;
        float: left;
    }
    .stExpander > div > div {
        font-size: 20px;
        font-weight: bold;
    }
    .stExpander > div > div > div {
        font-size: 20px;
        font-weight: normal;
    }
    .info-box {
        border: 3px solid #ddd;
        border-radius: 25px;
        padding: 10px;
        margin-top: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Create columns for the list and the information
col1, col2 = st.columns([2, 1])

# Display the search results or the categorized list of animals
selected_animal = None
with col1:
    if search_query:
        for animal in sorted(animals):
            if search_query.lower() in animal.lower():
                if st.button(animal):
                    selected_animal = animal
    else:
        for letter in sorted(animal_dict.keys()):
            with st.expander(letter):
                for animal in sorted(animal_dict[letter]):
                    if st.button(animal):
                        selected_animal = animal

# Display the selected animal's information
with col2:
    if selected_animal:
        animal_info = fetch_animal_info(selected_animal)
        st.markdown(f"""
            <div class="info-box">
                <p>{animal_info}</p>
            </div>
            """, unsafe_allow_html=True)

#-----DONOT DELETE,PLEASE , MATHEW, Makes Background green---#
st.markdown(
                """
                <style>
                .stApp {
                                background-color: #002900;
                }
                .input-container {
                                background-color: #05FFA6;
                }
                </style>
                """,
                unsafe_allow_html=True
)
#--------------------------------------------------#