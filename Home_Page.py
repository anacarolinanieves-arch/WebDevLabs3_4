import streamlit as st

# Title of App
st.title("Web Development Labs 03 & 04")

# Assignment Data
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 83 MedTechs, Web Development - Section A")
st.subheader("Ana Carolina Nieves Morales, Makailyn Briyanna Calhoun")

# TODO (optional): Add a group photo to the images folder and show it here, for example:
st.image("images/group_photo.jpg")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. Data Page: Explore interactive visualizations of official openFDA medical device data.
2. Chatbot: Chat with our AI assistant to ask general questions about medical device reliability, hospital technology, and equipment safety.
3. Agent: (Coming in Lab 4) An  AI data assistant that connects directly to our FDA medical device datasets to answer questions about manufacturer reliability, leading malfunction causes, and devices with the most reported issues.

""")
