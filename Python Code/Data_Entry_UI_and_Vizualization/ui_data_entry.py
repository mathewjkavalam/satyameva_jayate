# TODO: ask if each input should have separate submit buttons
'''salve, regina, mater misericordiae...
Take care of data entry
example:
>>animal_classification: Panthera tigris tigris
  image_url:/images/Bengal-tiger-220220251550.jpg
  location_latitude_logitude:41.85, -87.65
'''
from random import randint as id_generator
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
location = ui.text_input(
   label="Latitude, Logitude", value="41.85, -87.65")
latitude, logitude = location.replace(' ','').split(',')
latitude, logitude = float(latitude), float(logitude)
ui.write("Latitude:",str(latitude),",","Logitude:",str(logitude))
# caution: in production use id generator with better randomness!
capture_globally_unique_id = id_generator(1,10000000000000000000)
ui.divider()
ui.date_input(label= "Date of animal sighting", value= "default_value_today")
ui.time_input(label= "Time of animal sighting", value= "now")
ui.write("Capture ID:",capture_globally_unique_id)