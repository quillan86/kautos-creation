import streamlit as st

def display_complete_event_form(generator):
    st.header("Complete Existing Event")
    st.markdown("Flesh out details for an existing event in Kautos.")

    with st.form(key="complete_event_form"):
        event_name = st.text_input(
            "Event Name to Complete:", 
            help="Enter the exact name of the event you want to complete."
        )
        delta_year = st.number_input(
            "Delta Year for Contextual Events:", 
            step=1, value=100,
            help="Define the year offset for finding contextually similar events to help guide completion."
        )
        near = st.checkbox(
            "Use Near Locations for Context:", 
            value=True, 
            help="Consider events in locations near the original event\'s location for context."
        )
        symmetric = st.checkbox(
            "Symmetric Year Range for Context:", 
            value=True, 
            help="If checked, delta_year for context is applied both before and after the event\'s timeframe. If unchecked, it\'s applied only before."
        )
        
        submit_button = st.form_submit_button("Complete Event")

    if submit_button:
        if not event_name:
            st.error("Please enter an Event Name to complete.")
            return
        if delta_year is None:
            st.error("Please enter a Delta Year for context.")
            return

        with st.spinner("Completing event..."):
            try:
                result = generator.complete_event(
                    event_name=event_name, 
                    delta_year=int(delta_year),
                    near=near, 
                    symmetric=symmetric
                )
                st.session_state.event_result = result
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.event_result = None 