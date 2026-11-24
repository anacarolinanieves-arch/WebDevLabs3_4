# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import streamlit as st
from pydantic_ai import Agent

def askAgent(prompt, history):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(asyncio.run, chatAgent.run(prompt, message_history=history))
        return future.result()
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Missing GOOGLE_API_KEY in .streamlit/secrets.toml. Please add your key and reload.")

agentInstructions = (
    "You are a helpful hospital technology and medical device reliability assistant. "
    "Answer general questions about medical devices (such as infusion pumps, ventilators, "
    "patient monitors, and defibrillators), equipment safety, common malfunction causes, "
    "and quality engineering concepts. "
    "Stay strictly on this theme: if the user asks about an unrelated topic, politely "
    "remind them that you only discuss medical device reliability and hospital technology. "
    "Do not make up live statistics or claim to search the FDA database; if asked for "
    "exact recall counts or live records, explain that you cannot look up external data yet."
)

chatAgent = Agent("google:gemini-3.8-flash",instructions=agentInstructions)

st.title("Medical Device Reliability Chatbot")
st.write("Ask general questions about hospital medical devices, safety practices, and reliability.")

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chatMessages" not in st.session_state:
    st.session_state["chatMessages"] = []

if st.button("Clear Conversation"):
    st.session_state["message_history"] = []
    st.session_state["chatMessages"] = []

for msg in st.session_state["chatMessages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

userPrompt = st.chat_input("Ask a question about medical device reliability...")

if userPrompt:
    with st.chat_message("user"):
        st.write(userPrompt)
    st.session_state["chatMessages"].append({"role": "user", "content": userPrompt})
    try:
        result = askAgent(userPrompt, st.session_state["message_history"])
        botReply = result.output
        st.session_state["message_history"] = result.all_messages()

        with st.chat_message("assistant"):
            st.write(botReply)
        st.session_state["chatMessages"].append({"role": "assistant", "content": botReply})
    except Exception as err:
        st.error(f"Sorry, something went wrong while contacting the chatbot: {err}")
