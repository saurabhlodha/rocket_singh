import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Sorpetaler Sales Assistant",
    layout="wide"
)

# Initialize session state for messages if not exists
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        "id": "1",
        "content": "Hello! I'm your Sorpetaler Fensterbau sales assistant. How can I help you today?",
        "role": "assistant",
        "timestamp": str(datetime.now())
    }]

st.title("Sorpetaler Sales Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.write(f"You: {message['content']}")
        else:
            st.write(f"Assistant: {message['content']}")

# Chat input
user_input = st.text_input("Type your message:", key="user_input")

if st.button("Send"):
    if user_input:
        # Add user message to chat
        user_message = {
            "id": str(datetime.now().timestamp()),
            "content": user_input,
            "role": "user",
            "timestamp": str(datetime.now())
        }
        st.session_state.messages.append(user_message)

        try:
            # Send request to backend
            response = requests.post(
                "http://localhost:8000/api/chat",
                json={
                    "messages": [
                        {"content": msg["content"], "role": msg["role"]}
                        for msg in st.session_state.messages
                    ]
                }
            )
            
            if response.status_code == 200:
                assistant_response = response.json()
                # Add assistant response to chat
                assistant_message = {
                    "id": str(datetime.now().timestamp()),
                    "content": assistant_response["content"],
                    "role": "assistant",
                    "timestamp": str(datetime.now())
                }
                st.session_state.messages.append(assistant_message)
                st.rerun()
            else:
                st.error("Failed to get response from the assistant")
        except Exception as e:
            st.error(f"Error: {str(e)}")