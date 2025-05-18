import streamlit as st
import json

def display_output(result_data: dict):
    if not result_data:
        # You could add an st.info here if desired for when no result is present.
        # e.g., st.info("No event data to display. Generate an event first.")
        return

    st.subheader("Generated/Completed Event Details:")

    # Display Description if available
    description: str = result_data.get("description")
    if description:
        st.markdown("##### Description")
        st.text_area("Description (select and copy)", value=description, height=200, key="desc_text_area", help="You can select and copy the text from this area.")
        # Simple button, actual copy-to-clipboard needs more complex solutions in Streamlit
        # For now, this button serves as a visual cue or placeholder if you add JS later.
        # if st.button("Copy Description to Clipboard", key="copy_desc"):
        #     st.info("Please manually copy the description text above.") # Placeholder action

    # Display Excerpt if available
    excerpt: str = result_data.get("excerpt")
    if excerpt:
        st.markdown("##### Excerpt")
        st.text_area("Excerpt (select and copy)", value=excerpt, height=100, key="exce_text_area", help="You can select and copy the text from this area.")
        # if st.button("Copy Excerpt to Clipboard", key="copy_exce"):
        #     st.info("Please manually copy the excerpt text above.") # Placeholder action

    # Display Full JSON in an expander
    st.markdown("--- ") # Separator
    with st.expander("View Full Output JSON", expanded=False): # Set expanded=False by default
        st.json(result_data)

    # Alternative: If you want to keep the st.json display (which is collapsible and pretty)
    # st.markdown("--- ")
    # st.markdown("##### Full Output (Collapsible JSON View)")
    # with st.expander("View Full Output JSON", expanded=True):
    #     st.json(result_data)
    # If result_data is None (e.g., after an error or before first run for a task),
    # this function will do nothing, or you could add an st.info here if desired. 