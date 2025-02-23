import streamlit as st
from collections import defaultdict

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
    </style>
    """, unsafe_allow_html=True)

# Display the search results or the categorized list of animals
if search_query:
    for animal in sorted(animals):
        if search_query.lower() in animal.lower():
            st.write(animal)
else:
    for letter in sorted(animal_dict.keys()):
        with st.expander(letter):
            for animal in sorted(animal_dict[letter]):
                st.write(animal)