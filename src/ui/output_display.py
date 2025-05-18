import streamlit as st

def display_output(result_data):
    if result_data:
        st.subheader("Generated/Completed Event Details:")
        with st.expander("View Full Output JSON", expanded=True):
            st.json(result_data)
    # If result_data is None (e.g., after an error or before first run for a task),
    # this function will do nothing, or you could add an st.info here if desired. 