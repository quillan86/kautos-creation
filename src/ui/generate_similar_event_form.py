import streamlit as st
from src.backend.generator import Generator

def display_generate_similar_event_form(generator: Generator):
    st.header("Generate Similar Event")
    st.markdown("Create a new event in Kautos based on an existing one.")

    with st.form(key="generate_similar_event_form"):
        event_name = st.text_input(
            "Event Name to Base On:", 
            help="Enter the exact name of an existing event in Kautos."
        )
        delta_year = st.number_input(
            "Delta Year for Similarity:", 
            step=1, value=100, 
            help="Define the year offset for finding contextually similar events and influencing the new event\'s timeframe."
        )
        near = st.checkbox(
            "Search Near Locations for Context:", 
            value=True, 
            help="Consider events in locations near the original event\'s location for context."
        )
        symmetric = st.checkbox(
            "Symmetric Year Range for Context:", 
            value=True, 
            help="If checked, delta_year for context is applied both before and after the seed event\'s timeframe. If unchecked, it\'s applied only before."
        )
        
        submit_button = st.form_submit_button("Generate Similar Event")

    if submit_button:
        if not event_name:
            st.error("Please enter an Event Name to base on.")
            return
        if delta_year is None:
            st.error("Please enter a Delta Year.")
            return
            
        with st.spinner("Generating similar event..."):
            try:
                result = generator.generate_similar_event(
                    event_name=event_name, 
                    delta_year=int(delta_year),
                    near=near, 
                    symmetric=symmetric
                )
                st.session_state.event_result = result
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.event_result = None 