import logging
logger = logging.getLogger()

import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests
import time  # Import the time module

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

data = {}
userID = st.session_state['id']
try:
    data = requests.get(f'http://api:4000/u/users/{userID}').json()
except:
    st.write("**Important**: Could not connect to sample api, so using dummy data.")
    user_data = {"name":"Dummy Country", "z": {"b": "456", "c": "goodbye"}}

df = pd.DataFrame(data)

# # init fields with random data
# email = "test@gmail.com"
# age = 25
# phone = "123-456-7890"
# first_name = "John"
# last_name = "Doe"
# home_state = "California"
# move_load = "Full Household"

for index, rows in df.iterrows():
    email = rows['email']
    age = rows['age']
    phone = rows['phone']
    first_name = rows['firstName']
    last_name = rows['lastName']
    home_state = rows['homeStateID']
    move_load = rows['moveLoad']

load = data[0]['moveLoad']
if load == 'Full Household':
    loadIndex = 0
elif load == 'Part HouseHold':
    loadIndex = 1
elif load == 'Personal Effects Only':
    loadIndex = 2
elif load == 'Excess Baggage':
    loadIndex = 3
else:
    loadIndex = 4

state_name = requests.get(f'http://api:4000/c/get_stateName/{home_state}').json()[0]['stateName']

home_state_data = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", 
                                         "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
                                         "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", 
                                         "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", 
                                         "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", 
                                         "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", 
                                         "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
                                         "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
                                         "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
                                         "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
# Get the index of the state string where state_name equals the state name
state_index = home_state_data.index(state_name)

# User input fields
first_name = st.text_input("First Name", value=first_name)
last_name = st.text_input("Last Name", value=last_name)
email = st.text_input("Email", value=email)
phone_number = st.text_input("Phone Number", value=phone)
age = st.number_input("Age", min_value=0, max_value=120, step=1, value=age)
home_state = st.selectbox("Home State", home_state_data, index = state_index, placeholder="Select a state")

move_load = st.selectbox("Move Load", ['Full Household', 'Part Household', 'Personal Effects Only', 'Excess Baggage', 'Vehicle Only'], index = loadIndex, placeholder="Select a move load")




# Save button
if st.button("Save"):
    # Logic to save the user profile information
    stateID = requests.get(f'http://api:4000/c/get_stateID/{home_state}').json()[0]['id']
    data = {"first" : first_name,
            "last" : last_name,
            "email" : email,
            "phone" : phone_number,
            "age" : str(age),
            "stateID" : str(stateID),
            "load" : str(move_load),
            "id" : str(userID)}
    response = requests.put(f'http://api:4000/u/user_edit', json=data)
    if response.status_code == 200:
        st.success("Profile updated successfully!")
        time.sleep(1)  # Add a 1-second delay
        st.experimental_rerun()
