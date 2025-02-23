import streamlit as st
from collections import defaultdict
import sqlite3

# List of land animals from A-Z
animals = [
    "Aardvark", "Alpaca", "Ant", "Anteater", "Antelope", "Ape", "Armadillo", "Donkey",
    "Baboon", "Badger", "Bat", "Bear", "Beaver", "Bison", "Boar", "Buffalo",
    "Camel", "Capybara", "Caribou", "Cat", "Caterpillar", "Cattle", "Chamois", "Cheetah", "Chicken",
    "Chimpanzee", "Chinchilla", "Cobra", "Cockroach", "Coyote", "Crab",
    "Crocodile", "Crow", "Deer", "Dog", "Dogfish", "Dolphin", "Dove",
    "Dragonfly", "Duck", "Eagle", "Echidna", "Eel", "Eland", "Elephant", "Elk", "Emu",
    "Falcon", "Ferret", "Finch", "Flamingo", "Fly", "Fox", "Frog", "Gaur", "Gazelle", "Gerbil", "Giraffe",
    "Gnat", "Gnu", "Goat", "Goldfinch", "Goose", "Gorilla", "Goshawk", "Grasshopper", "Grouse", "Guanaco",
    "Gull", "Hamster", "Hare", "Hawk", "Hedgehog", "Heron", "Herring", "Hippopotamus", "Hornet", "Horse", "Human",
    "Hummingbird", "Hyena", "Ibex", "Ibis", "Jackal", "Jaguar", "Jay", "Jellyfish", "Kangaroo", "Kingfisher",
    "Koala", "Kookabura", "Kouprey", "Kudu", "Lapwing", "Lark", "Lemur", "Leopard", "Lion", "Llama", "Lobster",
    "Locust", "Loris", "Louse", "Lyrebird", "Magpie", "Mallard", "Manatee", "Mandrill", "Mantis", "Marten",
    "Meerkat", "Mink", "Mole", "Mongoose", "Monkey", "Moose", "Mosquito", "Mouse", "Mule", "Narwhal", "Newt",
    "Nightingale", "Octopus", "Okapi", "Opossum", "Oryx", "Ostrich", "Otter", "Owl", "Oyster", "Panther", "Parrot",
    "Partridge", "Peafowl", "Pelican", "Penguin", "Pheasant", "Pig", "Pigeon", "Pony", "Porcupine", "Porpoise",
    "Quail", "Quelea", "Quetzal", "Rabbit", "Raccoon", "Rail", "Ram", "Rat", "Raven", "Red deer", "Red panda",
    "Reindeer", "Rhinoceros", "Rook", "Salamander", "Salmon", "Sand Dollar", "Sandpiper", "Sardine", "Scorpion",
    "Seahorse", "Seal", "Shark", "Sheep", "Shrew", "Skunk", "Snail", "Snake", "Sparrow", "Spider", "Spoonbill",
    "Squid", "Squirrel", "Starling", "Stingray", "Stinkbug", "Stork", "Swallow", "Swan", "Tapir", "Tarsier",
    "Termite", "Tiger", "Toad", "Trout", "Turkey", "Turtle", "Viper", "Vulture", "Wallaby", "Walrus", "Wasp",
    "Weasel", "Whale", "Wildcat", "Wolf", "Wolverine", "Wombat", "Woodcock", "Woodpecker", "Worm", "Wren",
    "Yak", "Zebra"
] 

# Dictionary to map animals to their image URLs or file paths
animal_images = {
    "Tiger": "pages/22022025_1726.jpg",
    "Cat": "pages/1241251444.jpg",
    # Add paths or URLs for all animals
}

# Function to fetch animal information from the database
def fetch_animal_info(animal_name):
    animal_info_dict = {
        "Tiger": "Fun Fact:\nTigers are the largest living cats, reaching lengths of up to 13 ft (4 m) and weighing up to 300 kg.",
        "Cat":"Fun Fact:\nIsaac Newton is believed to have invented the cat door because his cats would scratch at the door while he worked.",
        # Add information for all animals
    }
    return animal_info_dict.get(animal_name, "Information not available.")
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
st.set_page_config(page_title="Animal List from A-Z", layout="wide")
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
    .info-box img {
        max-width: 100%;
        height: auto;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create columns for the list and the image
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

# Display the selected animal's image and information
with col2:
    if selected_animal:
        animal_info = fetch_animal_info(selected_animal)
        st.image(
            animal_images[selected_animal])
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