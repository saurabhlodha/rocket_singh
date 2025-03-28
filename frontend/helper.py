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

def show_settings():
    st.title("System Settings")

    try:
        # Load system prompt
        response = requests.get("http://localhost:8000/api/prompts/system_prompt")
        if response.status_code == 200:
            system_prompt = response.json()
            st.header("System Prompt")

            prompt_str = st.text_area(
                "System Prompt Text",
                value=system_prompt["content"],
                height=400
            )

            if st.button("Update System Prompt"):
                updated_prompt = {
                    "content": prompt_str
                }

                response = requests.put(
                    "http://localhost:8000/api/prompts/system_prompt",
                    json=updated_prompt
                )

                if response.status_code == 200:
                    st.success("System prompt updated successfully!")
                else:
                    st.error("Failed to update system prompt")

        # Load conversation flow
        response = requests.get("http://localhost:8000/api/prompts/conversation_flow")
        if response.status_code == 200:
            conversation_flow = response.json()

            st.header("Conversation Flow")
            flow_json = st.text_area(
                "Conversation Flow (JSON)",
                value=json.dumps(conversation_flow["content"], indent=2),
                height=400
            )

            if st.button("Update Conversation Flow"):
                try:
                    updated_flow = {
                        "content": json.loads(flow_json)
                    }

                    response = requests.put(
                        "http://localhost:8000/api/prompts/conversation_flow",
                        json=updated_flow
                    )

                    if response.status_code == 200:
                        st.success("Conversation flow updated successfully!")
                    else:
                        st.error("Failed to update conversation flow")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format")

    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
