import streamlit as st
import pydeck as pdk
import pandas as pd

# Expanded wildlife dataset with even more regions, species, and habitats
wildlife_data = {
    "Africa": {
        "species": ["African Elephant", "Lion", "Giraffe", "Cheetah", "Zebra", "Rhinoceros", "Buffalo"],
        "habitats": ["Savannah", "Rainforest", "Grasslands", "Desert", "Wetlands"]
    },
    "Amazon Rainforest": {
        "species": ["Jaguar", "Sloth", "Macaw", "Anaconda", "Capybara", "Poison Dart Frog", "Pygmy Marmoset"],
        "habitats": ["Rainforest", "Tropical", "Wetlands"]
    },
    "Australia": {
        "species": ["Kangaroo", "Koala", "Dingo", "Crocodile", "Platypus", "Wombat", "Emu"],
        "habitats": ["Outback", "Forest", "Grasslands", "Wetlands"]
    },
    "Siberia": {
        "species": ["Siberian Tiger", "Brown Bear", "Reindeer", "Snow Leopard", "Amur Leopard", "Musk Ox"],
        "habitats": ["Tundra", "Taiga", "Temperate Forest", "Steppe"]
    },
    "Madagascar": {
        "species": ["Ring-tailed Lemur", "Aye-aye", "Fossa", "Chameleon", "Giant Tortoise", "Madagascar Hissing Cockroach"],
        "habitats": ["Rainforest", "Spiny Forest", "Dry Forest", "Coastal"]
    },
    "Alaska": {
        "species": ["Grizzly Bear", "Moose", "Caribou", "Bald Eagle", "Arctic Fox", "Beaver", "Wolf"],
        "habitats": ["Tundra", "Boreal Forest", "Glaciers", "Wetlands"]
    },
    "Antarctica": {
        "species": ["Emperor Penguin", "Leopard Seal", "Weddell Seal", "Krill", "Antarctic Petrel", "Snow Petrel"],
        "habitats": ["Polar Desert", "Ice Shelves", "Ocean"]
    },
    "North America": {
        "species": ["American Bison", "Gray Wolf", "Mountain Lion", "American Alligator", "Beaver", "Peregrine Falcon"],
        "habitats": ["Temperate Forest", "Grasslands", "Wetlands", "Desert", "Tundra"]
    },
    "Europe": {
        "species": ["European Brown Bear", "Red Fox", "European Bison", "Wild Boar", "Gray Wolf", "Eurasian Lynx"],
        "habitats": ["Temperate Forest", "Alpine", "Steppe", "Wetlands"]
    },
    "South America": {
        "species": ["Andean Condor", "Llama", "Puma", "Capybara", "Giant River Otter", "Spectacled Bear"],
        "habitats": ["Andes Mountains", "Rainforest", "Savannah", "Grasslands"]
    },
    "Asia": {
        "species": ["Giant Panda", "Tiger", "Indian Elephant", "Snow Leopard", "Red Panda", "Asian Elephant"],
        "habitats": ["Temperate Forest", "Bamboo Forest", "Mountainous", "Tropical Rainforest"]
    },
    "New Zealand": {
        "species": ["Kiwi", "Kea", "Takahe", "New Zealand Sea Lion", "Eel", "Fur Seal"],
        "habitats": ["Rainforest", "Coastal", "Grasslands", "Alpine"]
    }
}

# Coordinates for each region (adjust as needed)
region_coordinates = {
    "Africa": [0, 20],  # Latitude, Longitude for Africa
    "Amazon Rainforest": [-3.4653, -62.2159],  # Amazon
    "Australia": [-25.2744, 133.7751],  # Australia
    "Siberia": [60.0, 100.0],  # Siberia
    "Madagascar": [-18.7669, 46.8691],  # Madagascar
    "Alaska": [61.3713, -149.1100],  # Alaska
    "Antarctica": [-75.2500, -0.7111],  # Antarctica
    "North America": [40.7128, -74.0060],  # New York, USA
    "Europe": [48.8566, 2.3522],  # Paris, France
    "South America": [-23.5505, -46.6333],  # São Paulo, Brazil
    "Asia": [35.6762, 139.6503],  # Tokyo, Japan
    "New Zealand": [-40.9006, 174.8869],  # New Zealand
}

def display_wildlife_info(region):
    """Display wildlife species and their habitats for a selected region."""
    if region in wildlife_data:
        st.write(f"### Wildlife Species in {region}:")
        st.write(f"Species: {', '.join(wildlife_data[region]['species'])}")
        st.write(f"Habitat: {', '.join(wildlife_data[region]['habitats'])}")
    else:
        st.write("No information available for this region.")

def plot_3d_map(region):
    """Generate a 3D map with a region pin based on the selected region."""
    # Get the coordinates for the selected region
    if region in region_coordinates:
        lat, lon = region_coordinates[region]
    else:
        lat, lon = 0, 20  # Default to Africa if the region is not found

    # Initial view state of the map
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=4, pitch=60)

    # Creating the map layer with just one pin for the selected region
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=[{'lat': lat, 'lon': lon, 'region': region}],
        get_position='[lon, lat]',
        get_radius=500000,  # Radius for the pin
        get_color=[255, 0, 0, 160],  # Red color for the pin
        pickable=True
    )

    # Create the deck (3D map)
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{region}"},
        map_style='mapbox://styles/mapbox/outdoors-v11',  # Mapbox style
        api_keys={'mapbox': 'YOUR_MAPBOX_ACCESS_TOKEN'}  # Provide your Mapbox token
    )
    return r

# Streamlit app setup
st.title("3D Wildlife Map Viewer")
st.write("""
This application displays wildlife species information based on the region you select on the 3D map.
You can pin a region like Africa, Amazon Rainforest, Australia, Siberia, Madagascar, Alaska, Antarctica, North America, Europe, South America, Asia, or New Zealand to view the species and habitats there.
""")

# Sidebar with Region Selection
region = st.sidebar.selectbox("Select a Region", [
    "Africa", 
    "Amazon Rainforest", 
    "Australia", 
    "Siberia", 
    "Madagascar", 
    "Alaska", 
    "Antarctica", 
    "North America", 
    "Europe", 
    "South America", 
    "Asia", 
    "New Zealand"
])

# Display the 3D Map for the selected region
st.pydeck_chart(plot_3d_map(region))

# Display Wildlife Information for the selected region
display_wildlife_info(region)
