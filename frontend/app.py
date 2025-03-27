import streamlit as st
from helper import show_chat_interface, show_conversation_list, show_settings, create_new_project
import os

st.set_page_config(
    page_title="Sales Agent Chatbot Platform",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = None
if 'view' not in st.session_state:
    st.session_state.view = 'projects'  # projects, chat, list, settings, or detail
if 'current_project' not in st.session_state:
    st.session_state.current_project = None

# Navigation
col1, col2, col3, col4 = st.columns([1, 1, 1, 7])
with col1:
    if st.button("🏠 Projects"):
        st.session_state.view = 'projects'
        st.rerun()
with col2:
    if st.session_state.current_project and st.button("📝 Chat" if st.session_state.view != 'chat' else "📋 List"):
        st.session_state.view = 'list' if st.session_state.view == 'chat' else 'chat'
        st.rerun()
with col3:
    if st.session_state.current_project and st.button("⚙️ Settings"):
        st.session_state.view = 'settings'
        st.rerun()

# Show the appropriate view
if st.session_state.view == 'projects':
    st.title("Sales Agent Chatbot Platform")

    # Create new project form
    with st.form("new_project"):
        st.write("Create New Sales Agent Chatbot")
        project_name = st.text_input("Project Name (lowercase, no spaces)")
        submitted = st.form_submit_button("Create Project")

        if submitted and project_name:
            if project_name.islower() and " " not in project_name:
                success = create_new_project(project_name)
                if success:
                    st.success(f"Project {project_name} created successfully!")
                    st.session_state.current_project = project_name
                    st.session_state.view = 'chat'
                    st.rerun()
            else:
                st.error("Project name must be lowercase without spaces")

    # List existing projects
    st.subheader("Existing Projects")
    projects_dir = "projects"
    if os.path.exists(projects_dir):
        projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
        for project in projects:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(project)
            with col2:
                if st.button("Open", key=f"open_{project}"):
                    st.session_state.current_project = project
                    st.session_state.view = 'chat'
                    st.rerun()
    else:
        st.write("No projects found")

elif st.session_state.view == 'chat':
    show_chat_interface()
elif st.session_state.view == 'settings':
    show_settings()
else:
    show_conversation_list()
