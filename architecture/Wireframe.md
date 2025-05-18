# Kautos Event Generator - Streamlit UI Wireframe

This document outlines the wireframe for a Streamlit-based user interface for interacting with the Kautos event generation and completion tools.

## 1. Overall Layout

The UI will consist of two main sections:

*   **A. Sidebar (Navigation & Task Selection):**
    *   Located on the left side of the screen.
    *   Used for selecting the primary generation task.
*   **B. Main Content Area (Inputs & Outputs):**
    *   Occupies the rest of the screen.
    *   Dynamically displays input fields based on the task selected in the sidebar.
    *   Displays the results of the generation task.

## 2. Sidebar: Task Selection

*   **Component:** `st.sidebar.radio` or `st.sidebar.selectbox`
*   **Label:** "Select Task"
*   **Options:**
    *   "Generate Similar Event" (Corresponds to `generate_similar_event`)
    *   "Complete Existing Event" (Corresponds to `complete_event`)
    *   "Generate New Event in Range" (Corresponds to `generate_event_in_range`)
    *   *(A note indicating this list can be expanded with future tasks)*
*   **Behavior:** Selecting an option in the sidebar will change the input form displayed in the Main Content Area.

## 3. Main Content Area: Input Forms & Output

The Main Content Area will be divided into two sub-sections:
    *   **3.1. Task-Specific Input Form:** (Dynamically rendered based on sidebar selection)
    *   **3.2. Output Display:** (Shows results after form submission)

### 3.1. Task-Specific Input Forms

Each task will have its own form (`st.form`) to group its specific input fields and a submission button.

#### 3.1.1. Form: Generate Similar Event

*   **Title:** `st.header("Generate Similar Event")`
*   **Description:** `st.markdown("Create a new event in Kautos based on an existing one.")`
*   **Input Fields:**
    *   `Event Name to Base On:` (`st.text_input`, help="Enter the exact name of an existing event in Kautos.")
    *   `Delta Year for Similarity:` (`st.number_input`, step=1, help="Define the year offset for finding contextually similar events and influencing the new event's timeframe.")
    *   `Search Near Locations:` (`st.checkbox`, value=True, help="Consider events in locations near the original event's location for context.")
    *   `Symmetric Year Range for Context:` (`st.checkbox`, value=True, help="If checked, delta_year is applied both before and after the seed event's timeframe. If unchecked, it's applied only before.")
*   **Submit Button:** `st.form_submit_button("Generate Similar Event")`

#### 3.1.2. Form: Complete Existing Event

*   **Title:** `st.header("Complete Existing Event")`
*   **Description:** `st.markdown("Flesh out details for an existing event in Kautos.")`
*   **Input Fields:**
    *   `Event Name to Complete:` (`st.text_input`, help="Enter the exact name of the event you want to complete.")
    *   `Delta Year for Contextual Events:` (`st.number_input`, step=1, help="Define the year offset for finding contextually similar events to help guide completion.")
    *   `Use Near Locations for Context:` (`st.checkbox`, value=True, help="Consider events in locations near the original event's location for context.")
    *   `Symmetric Year Range for Context:` (`st.checkbox`, value=True, help="If checked, delta_year for context is applied both before and after the event's timeframe. If unchecked, it's applied only before.")
*   **Submit Button:** `st.form_submit_button("Complete Event")`

#### 3.1.3. Form: Generate New Event in Range

*   **Title:** `st.header("Generate New Event in Range")`
*   **Description:** `st.markdown("Create a brand new event within a specified time period and location in Kautos.")`
*   **Input Fields:**
    *   `st.subheader("Define New Event's Parameters:")`
    *   `New Event Start Year:` (`st.number_input`, step=1, help="The year the new event should begin.")
    *   `New Event End Year:` (`st.number_input`, step=1, help="The year the new event should end. Can be same as start year for punctual events.")
    *   `Location for New Event:` (`st.text_input`, help="Specify the primary location name for the new event.")
    *   `st.subheader("Define Contextual Search Parameters (for inspiration):")`
    *   `Contextual Events Start Year:` (`st.number_input`, step=1, help="Start year of the range to search for existing events for context.")
    *   `Contextual Events End Year:` (`st.number_input`, step=1, help="End year of the range to search for existing events for context.")
    *   `Use Near Locations for Context:` (`st.checkbox`, value=True, help="Consider events in locations near the specified 'Location for New Event' for context.")
*   **Submit Button:** `st.form_submit_button("Generate Event in Range")`

### 3.2. Output Display

*   **Conditional Title:**
    *   If an event is generated/completed: `st.subheader("Generated/Completed Event Details:")`
*   **Content:**
    *   The resulting event dictionary will be displayed using `st.json()`.
    *   This could be wrapped in an `st.expander("View Raw Output")` for cleaner presentation if the JSON is large.
*   **Placeholder:** If no task has been run yet, a message like `st.info("Select a task from the sidebar and fill in the details to generate an event.")` can be shown.

## 4. Status Indicators and Error Handling

*   **Loading:** When a generation task is in progress (after a submit button is clicked and before results are returned), a `st.spinner("Generating event...")` or similar message should be displayed.
*   **Errors:** If the backend process encounters an error (e.g., API issues, validation problems), a clear error message should be displayed using `st.error("An error occurred: [error details]")`.

## 5. Expandability Notes

*   The sidebar task selection naturally allows adding new tasks. Each new task would involve:
    1.  Adding a new option to the radio/select group in the sidebar.
    2.  Creating a new corresponding input form function/section in the main content area.
    3.  Ensuring the backend `generator.py` method is called appropriately.
*   Input fields within forms can be added or modified as the underlying generator functions evolve.
