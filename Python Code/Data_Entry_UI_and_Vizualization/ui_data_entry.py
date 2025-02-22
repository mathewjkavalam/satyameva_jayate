'''salve, regina, mater misericordiae...
Take care of data entry
example:
>>animal_classification: Panthera tigris tigris
  image_url:/images/Bengal-tiger-220220251550.jpg
  location_latitude_logitude:41.85, -87.65
'''
import streamlit as ui

# TODO: connect with DB to save the input for later
animal_classification = ui.text_input(
    label="Animal classification", value="Panthera tigris tigris")