import streamlit as st
import json
import requests
import SessionState
from datetime import datetime

st.set_page_config(
        page_title="My Class",
        page_icon="📚"
        # layout="wide",
        initial_sidebar_state="expanded"
    )

add_selectbox = st.sidebar.selectbox(
    "Class",
    ("Classes 1-3", "4th Class", "5th Class", "6th Class", "7th Class", "8th Class", "9th Class", "10th Class"),
    index=1
)

# To cache the data for 1 Day
session_state = SessionState.get(data=None,last_updated=None,days=0)

now = datetime.now()
if session_state.last_updated is not None:
    lastUpdate = session_state.last_updated
    session_state.days = (now -lastUpdate).days

if session_state.last_updated is None or session_state.days >=1:
    response = requests.get("https://raw.githubusercontent.com/arjunraghurama/1-10-classes/main/data/data.json")
    url_data = json.loads(response.text)
    session_state.data = url_data
    session_state.last_updated = now
        
# response = requests.get("https://raw.githubusercontent.com/arjunraghurama/1-10-classes/main/data/data.json")
# data = json.loads(response.text)

video_list = session_state.data[add_selectbox]
for i in range(len(video_list)):
    st.header(str(1+i)+ ". " + video_list[i][1])
    st.video(video_list[i][2])
