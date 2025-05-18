import streamlit as st

def display_sidebar():
    st.sidebar.title("Kautos Event Tools")
    task_options = [
        "Generate Similar Event", 
        "Complete Existing Event", 
        "Generate New Event in Range"
    ]
    selected_task = st.sidebar.radio(
        "Select Task", 
        task_options, 
        index=None # No default selection
    )
    st.sidebar.markdown("---_Future tasks can be added here_---")
    return selected_task 