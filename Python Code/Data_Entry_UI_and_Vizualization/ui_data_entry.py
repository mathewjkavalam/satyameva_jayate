'''salve, regina, mater misericordiae...
Take care of data entry
example:
>>animal_classification: Panthera tigris tigris
  image_url:/images/Bengal-tiger-220220251550.jpg
  location_latitude_longitude:41.85, -87.65
'''
from random import randint as id_generator
import streamlit as ui

def  get_latitude_logitude_from_location_name(location_name :str):
    return {"lat":41.85, "lng":-87.65}
def compute_list_of_time_to_populate_dropdown_ui():
  # TODO: may need to tweak the now because the edge case is
  # problematic
  from datetime import datetime, timedelta

  # Get the current time
  now = datetime.now()

  # Start from midnight
  start_time = datetime(now.year, now.month, now.day, 0, 0)

  # List to hold the time tuples
  time_list = []

  # Generate times in 30-minute intervals
  current_time = start_time
  while current_time <= now:
      time_tuple = (current_time.strftime("%H:%M"),)
      time_list.append(time_tuple)
      current_time += timedelta(minutes=15)

  return time_list

ui.write("Upload Animal Sighting")
animal_classification = "" 
# TODO: connect with DB to save the input for later
# store the uploaded image locally, so that it can be previewed
animal_image = ui.file_uploader(
    label="Choose the image of the animal", accept_multiple_files=False)
if animal_image is None:
    pass
else:
  ui.image(image= animal_image)
region = ui.text_input(
   label= "Region", value= "", help ="example: Donmouth Local Natural Reserve"
)
# TODO:get the API for location set-up
location = get_latitude_logitude_from_location_name(location_name= region)
latitude, longitude = location["lat"], location["lng"]
latitude, longitude = float(latitude), float(longitude)
# caution: in production use id generator with better randomness!
# Ensure the capture ID persists across inputs
if "capture_globally_unique_id" not in ui.session_state:
    ui.session_state.capture_globally_unique_id = id_generator(1, 10000000000000000000)

capture_globally_unique_id = ui.session_state.capture_globally_unique_id
ui.divider()
from datetime import datetime, timedelta

# Get the current time
today_date = datetime.today()

ui.date_input(label= "Date of animal sighting", value= "today",max_value= today_date )
valid_time_list = compute_list_of_time_to_populate_dropdown_ui()
ui.selectbox("Time of animal sighting", valid_time_list)
ui.write("Capture ID:",capture_globally_unique_id)
# Submit Button to save the sighting
submit_button = ui.button("Submit Sighting")

if submit_button:
    # TODO: Connect to a database to save the data
    ui.write("Sighting submitted successfully!")
    # You can insert your DB saving logic here