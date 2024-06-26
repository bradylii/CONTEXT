import logging
logger = logging.getLogger()

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.nav import SideBarLinks
from streamlit_modal import Modal
import requests
import json
from datetime import datetime
import time
# Show appropriate sidebar links for the role of the currently logged in user
st.set_page_config(layout='wide')
SideBarLinks()
companyID = st.session_state['companyID']
mcData = requests.get(f'http://api:4000/mv/moving_company/{companyID}').json()

companyName = mcData[0]['moverName']
userID = st.session_state['userID'] 
routeID = st.session_state['routeID']
countryName = st.session_state['countryName']
fromStateName = st.session_state['stateName']
name = st.session_state['name']

data = requests.get(f'http://api:4000/u/users/{userID}').json()
stateID = data[0]['homeStateID']
fromStateName = requests.get(f'http://api:4000/c/get_stateName/{stateID}').json()[0]['stateName']

if st.session_state['role'] == 'moving_company':
   fromStateName = '(STATE)'
   countryName = '(COUNTRY)'
   name = '(USER)'

data = {}

st.title(f"{companyName}")
st.write(f"Welcome to our page **{name}**, we would love to help you move from **{fromStateName}** to **{countryName}**")
st.image('https://www.xero.com/content/dam/xero/pilot-images/guides/us-guides/moving-business-header.1695098128416.png')


if st.button(f"Join Our Mail and Call List"):
      data = {"userID" : userID, 
              "moverID" : companyID, 
              "routeID" : routeID
              }
      try:
        response = requests.post('http://api:4000/mv/userContact', json=data)
        modal = Modal(key="success", title="Thank you for choosing " + companyName + "!")
      except:
        modal = Modal(key="something went wrong!", title="ERROR!")
      with modal.container():
        st.markdown("Expect to hear from us shortly")
      st.write(response)


email = mcData[0]['email']
phone = mcData[0]['phone']
bio = mcData[0]['bio']
numStars = mcData[0]['stars']
numReviews = mcData[0]['numReviews']

st.write('## learn more about us below!')
st.write(bio)
st.write('## Hesitant to contact us?')
st.write(f'Phone: {phone}')
st.write(f'email: {email}')
st.write("Stars: "+ ("⭐" * numStars) + "    " +str(numReviews) + " reviews")



