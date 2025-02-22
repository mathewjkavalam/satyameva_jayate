# TODO: ask if each input should have separate submit buttons
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

# TODO: ask if multiple file upload is priority
# store the uploaded image locally, so that it can be previewed
animal_image = ui.file_uploader(
    label="Choose the image of the animal", accept_multiple_files=False)
if animal_image is None:
    pass
else:
  ui.image(image= animal_image)