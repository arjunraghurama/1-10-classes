import streamlit as st
import json
import requests
import SessionState

st.set_page_config(
        page_title="My Class",
        # layout="wide",
        initial_sidebar_state="expanded"
    )

add_selectbox = st.sidebar.selectbox(
    "Class",
    ("Classes 1-3", "4th Class", "5th Class", "6th Class", "7th Class", "8th Class", "9th Class", "10th Class"),
    index=1
)

response = requests.get("https://raw.githubusercontent.com/arjunraghurama/1-10-classes/main/data/data.json")
data = json.loads(response.text)
video_list = data[add_selectbox]
for i in range(len(video_list)):
    st.header(str(1+i)+ ". " + video_list[i][1])
    st.video(video_list[i][2])
