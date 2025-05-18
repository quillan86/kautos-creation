import streamlit as st
from src.backend.generator import Generator

def display_generate_event_in_range_form(generator: Generator):
    st.header("Generate New Event in Range")
    st.markdown("Create a brand new event within a specified time period and location in Kautos.")

    with st.form(key="generate_event_in_range_form"):
        st.subheader("Define New Event's Parameters:")
        new_event_start_year = st.number_input(
            "New Event Start Year:", 
            step=1, value=-1000,
            help="The year the new event should begin."
        )
        new_event_end_year = st.number_input(
            "New Event End Year:", 
            step=1, value=-990,
            help="The year the new event should end. Can be same as start year for punctual events."
        )
        location_new_event = st.text_input(
            "Location for New Event:", 
            help="Specify the primary location name for the new event."
        )
        
        st.subheader("Define Contextual Search Parameters (for inspiration):")
        context_start_year = st.number_input(
            "Contextual Events Start Year:", 
            step=1, value=-1200,
            help="Start year of the range to search for existing events for context."
        )
        context_end_year = st.number_input(
            "Contextual Events End Year:", 
            step=1, value=-800,
            help="End year of the range to search for existing events for context."
        )
        near_context = st.checkbox(
            "Use Near Locations for Context (for inspiration search):", 
            value=True, 
            help="Consider events in locations near the specified 'Location for New Event' for contextual inspiration."
        )
        
        submit_button = st.form_submit_button("Generate Event in Range")

    if submit_button:
        if not location_new_event:
            st.error("Please specify a Location for the new event.")
            return
        if new_event_start_year is None or new_event_end_year is None or \
           context_start_year is None or context_end_year is None:
            st.error("Please ensure all year fields are entered.")
            return
        if new_event_end_year < new_event_start_year:
            st.error("New Event End Year cannot be before New Event Start Year.")
            return
        if context_end_year < context_start_year:
            st.error("Contextual Events End Year cannot be before Contextual Events Start Year.")
            return

        with st.spinner("Generating event in range..."):
            try:
                result = generator.generate_event_in_range(
                    start_year=int(new_event_start_year),
                    end_year=int(new_event_end_year),
                    range_start_year=int(context_start_year),
                    range_end_year=int(context_end_year),
                    location=location_new_event,
                    near=near_context
                )
                st.session_state.event_result = result
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.event_result = None 