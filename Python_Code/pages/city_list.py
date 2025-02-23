import streamlit as st
from collections import defaultdict

# List of cities from A-Z
cities = [
    "Amsterdam", "Athens", "Bangkok", "Barcelona", "Beijing", "Berlin", "Bogota", "Brussels",
    "Buenos Aires", "Cairo", "Cape Town", "Caracas", "Chicago", "Copenhagen", "Delhi", "Dubai",
    "Dublin", "Frankfurt", "Geneva", "Hanoi", "Helsinki", "Hong Kong", "Istanbul", "Jakarta",
    "Jerusalem", "Johannesburg", "Kuala Lumpur", "Lagos", "Lima", "Lisbon", "London", "Los Angeles",
    "Madrid", "Manila", "Mexico City", "Milan", "Moscow", "Mumbai", "Nairobi", "New York", "Oslo",
    "Paris", "Prague", "Rio de Janeiro", "Rome", "San Francisco", "Santiago", "Sao Paulo", "Seoul",
    "Shanghai", "Singapore", "Stockholm", "Sydney", "Taipei", "Tehran", "Tokyo", "Toronto", "Vienna",
    "Warsaw", "Washington D.C.", "Zurich" 
]

# Dictionary to map cities to their image URLs or file paths
city_images = {
    "Amsterdam": "pages/amsterdam.jpg",
    "Athens": "path_or_url_to_athens_image",
    "Tokyo": "pages/tokyo.jpg",
    # Add paths or URLs for all cities
}

# Dictionary to map cities to their information
city_info = {
    "Amsterdam": "Short Info. Animal Sightings. Graph View",
    "Athens": "Short Info. Animal Sightings. Graph View",
    "Tokyo": "Short Info. Animal Sightings. Graph View",
    # Add information for all cities
}

# Categorize cities by their starting alphabet
city_dict = defaultdict(list)
for city in cities:
    city_dict[city[0]].append(city)

# Streamlit app
st.set_page_config(page_title="City List from A-Z", layout="wide")
st.title("City List from A-Z")
 
# Add a search bar
search_query = st.text_input("Search for a city:")

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

# Display the search results or the categorized list of cities
selected_city = None
with col1:
    if search_query:
        for city in sorted(cities):
            if search_query.lower() in city.lower():
                if st.button(city):
                    selected_city = city
    else:
        for letter in sorted(city_dict.keys()):
            with st.expander(letter):
                for city in sorted(city_dict[letter]):
                    if st.button(city):
                        selected_city = city

# Display the selected city's image and information
with col2:
    if selected_city:
        st.image(
            city_images[selected_city])
        st.markdown(f"""
            <div class="info-box">
                <p>{city_info[selected_city]}</p>
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