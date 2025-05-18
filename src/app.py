import streamlit as st
from src.backend.generator import Generator
from src.ui.sidebar import display_sidebar
from src.ui.generate_similar_event_form import display_generate_similar_event_form
from src.ui.complete_event_form import display_complete_event_form
from src.ui.generate_event_in_range_form import display_generate_event_in_range_form
from src.ui.output_display import display_output

st.set_page_config(layout="wide", page_title="Kautos Event Generator")

@st.cache_resource
def get_generator():
    return Generator()

generator = get_generator()

def main():
    st.title("Kautos Event Generator")

    # Initialize session state for storing results
    if 'event_result' not in st.session_state:
        st.session_state.event_result = None

    selected_task = display_sidebar()

    if selected_task == "Generate Similar Event":
        display_generate_similar_event_form(generator)
    elif selected_task == "Complete Existing Event":
        display_complete_event_form(generator)
    elif selected_task == "Generate New Event in Range":
        display_generate_event_in_range_form(generator)
    else:
        st.info("Select a task from the sidebar to begin.")

    if st.session_state.event_result:
        display_output(st.session_state.event_result)

if __name__ == "__main__":
    main()
