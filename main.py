import streamlit as st
import json
import requests
import SessionState
from datetime import datetime

st.set_page_config(
        page_title="My Class",
        page_icon="📚",
        # layout="wide",
        initial_sidebar_state="expanded"
    )
classes = ["Classes 1-3", "4th Class", "5th Class", "6th Class", "7th Class", "8th Class", "9th Class", "10th Class"]
add_selectbox = st.sidebar.selectbox(
    "ತರಗತಿ",
    classes,
    index=1
)

classes_alt = ["1-3", "4", "5", "6", "7", "8", "9", "10"]
index = classes.index(add_selectbox) 
st.title("ತರಗತಿ {}".format(classes_alt[index]))

# To cache the data for 1 Day
session_state = SessionState.get(data=None,last_updated=None,hours=0)

now = datetime.now()
if session_state.last_updated is not None:
    lastUpdate = session_state.last_updated
    session_state.hours = ((now - lastUpdate).seconds)/(60*60)

if session_state.last_updated is None or session_state.hours >= 10:
    response = requests.get("https://raw.githubusercontent.com/arjunraghurama/1-10-classes/main/data/data.json")
    url_data = json.loads(response.text)
    session_state.data = url_data
    session_state.last_updated = now
        
video_list = session_state.data[add_selectbox]
for i in range(len(video_list)-1, -1, -1):
    st.header("ಪಾಠ " + str(1+i)+ " : " + video_list[i][1])
    st.video(video_list[i][2])
