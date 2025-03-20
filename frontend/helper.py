import streamlit as st
import requests
import json
from datetime import datetime

def load_conversation(conversation_id):
    response = requests.get(f"http://localhost:8000/api/conversations/{conversation_id}")
    if response.status_code == 200:
        conversation = response.json()
        st.session_state.messages = [
            {
                "id": idx,
                "content": msg["content"],
                "role": msg["role"],
                "timestamp": msg["timestamp"]
            }
            for idx, msg in enumerate(conversation["messages"])
        ]
        st.session_state.conversation_id = conversation_id
        st.session_state.view = 'chat'

def show_chat_interface():
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
                        "conversation_id": st.session_state.conversation_id,
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
                    st.session_state.conversation_id = assistant_response["conversation_id"]
                    st.rerun()
                else:
                    st.error("Failed to get response from the assistant")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_conversation_list():
    st.title("Conversations")
    
    if st.button("New Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.session_state.view = 'chat'
        st.rerun()

    try:
        response = requests.get("http://localhost:8000/api/conversations")
        if response.status_code == 200:
            conversations = response.json()
            for conv in conversations:
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    st.write(conv["started_at"][:10])
                with col2:
                    st.write(conv["last_message"][:100] + "..." if conv["last_message"] else "No messages")
                with col3:
                    if st.button("View", key=f"view_{conv['id']}"):
                        load_conversation(conv["id"])
                        st.rerun()
                st.divider()
    except Exception as e:
        st.error(f"Error loading conversations: {str(e)}")
