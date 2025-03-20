import streamlit as st
from helper import show_chat_interface, show_conversation_list

st.set_page_config(
    page_title="Sorpetaler Sales Assistant",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = None
if 'view' not in st.session_state:
    st.session_state.view = 'chat'  # chat, list, or detail

# Navigation
col1, col2 = st.columns([1, 9])
with col1:
    if st.button("📝 Chat" if st.session_state.view != 'chat' else "📋 List"):
        st.session_state.view = 'list' if st.session_state.view == 'chat' else 'chat'
        st.rerun()

# Show the appropriate view
if st.session_state.view == 'chat':
    show_chat_interface()
else:
    show_conversation_list()