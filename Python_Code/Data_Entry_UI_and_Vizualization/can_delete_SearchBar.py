'''
Search the different locations available in the dataset
'''
import streamlit as ui
import pandas as pd


def get_animal_sighting_for_the_region_name(region_name: str):
    # returns after filterimg the data by region name
    # Lion | Tiger
    # 3    | 1
    #--------------
    mock_data = {
        "Region": ["Aberdeen", "Aberdeen", "Aberdeen", "Aberdeen", "Aberdeen", "Aberdeen", "Aberdeen"],
        "Animal": ["Lion", "Tiger", "Elephant", "Giraffe", "Panda", "Kangaroo", "Zebra"],
        "Count": [3, 1, 2, 4, 5, 6, 3]
    }

    return pd.DataFrame(mock_data)

sightings_logged = get_animal_sighting_for_the_region_name("Aberdeen")

ui.dataframe(sightings_logged, width=1000, height=500)
