# Kautos Creation Platform

This project provides a platform for generating and managing historical events for the fictional world of Kautos. It leverages a Notion database as a backend for storing event data and uses an LLM for creative event generation tasks.

The platform is accessed via a Streamlit-based web interface.

## Core Features

*   **Event Data Management:** (Implicitly through `src/backend/events.py`) Interacts with a Notion database to retrieve and parse event, location, and polity data.
*   **LLM-Powered Event Generation:** Utilizes a Large Language Model (`src/backend/llm.py` and `src/backend/generator.py`) for:
    *   Generating new events similar to existing ones.
    *   Completing and fleshing out details for partially described events.
    *   Generating entirely new events within a specified time range and location.
*   **Schema Enforcement:** Uses Pydantic models (`src/backend/schemas.py`) to define the structure of events, locations, and polities, ensuring data consistency for LLM interactions.
*   **Interactive Web UI:** A Streamlit application (`src/app.py` and components in `src/ui/`) provides a user-friendly interface for all generation tasks.

## UI Overview (Based on Wireframe)

The Streamlit UI (`src/app.py`) is structured as follows:

*   **Sidebar Navigation:** Allows users to select the desired task:
    *   Generate Similar Event
    *   Complete Existing Event
    *   Generate New Event in Range
*   **Main Content Area:**
    *   Dynamically displays input forms tailored to the selected task.
    *   Shows the JSON output of the generated or completed event.
    *   Includes status indicators (spinners) and error handling.

### Key UI Components:

*   **`src/ui/sidebar.py`**: Manages the task selection in the sidebar.
*   **`src/ui/generate_similar_event_form.py`**: Provides the form for generating events based on an existing one.
*   **`src/ui/complete_event_form.py`**: Provides the form for completing an existing event.
*   **`src/ui/generate_event_in_range_form.py`**: Provides the form for generating a new event within a specific time and location.
*   **`src/ui/output_display.py`**: Handles the presentation of the results.

## Backend Logic

*   **`src/backend/events.py`**: Handles all interactions with the Notion API for fetching and parsing event, location, and polity data.
*   **`src/backend/schemas.py`**: Defines the Pydantic data models for `Event`, `Location`, `Polity`, and related Enums (`BiomeEnum`, `EventTypeEnum`). These schemas are crucial for structuring data passed to and received from the LLM.
*   **`src/backend/llm.py`**: Provides the interface to the Large Language Model used for generation tasks.
*   **`src/backend/generator.py`**: Orchestrates the event generation and completion processes. It crafts specific prompts for the LLM, prepares the input data (including contextual events), and calls the LLM with appropriate tools and schemas.
*   **`src/backend/constants.py`**: Stores constants like API keys and database IDs (ensure this is configured locally and kept out of version control if sensitive).

## Goals

*   Ability to generate new timeline events based on past ones.
*   Provide an intuitive UI for interacting with event generation tools.
*   Maintain a structured and extensible codebase for future enhancements.

## Setup & Running

There are two primary ways to set up and run the Kautos Creation Platform:

**Method 1: Local Development (using `uv` and direct execution)**

1.  **Prerequisites:** 
    *   Python 3.12 (as specified in `pyproject.toml`)
    *   [uv](https://github.com/astral-sh/uv) (Python package installer and resolver, `pip install uv` if not already installed)
2.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd kautos-creation
    ```
3.  **Create Virtual Environment and Install Dependencies:** `uv` will use the `pyproject.toml` to set up the environment and install dependencies.
    ```bash
    uv sync
    ```
4.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
    (On Windows, use `.venv\Scripts\activate`)
5.  **Configure Constants via `.env` file:** 
    *   Create a `.env` file in the project root directory (e.g., `kautos-creation/.env`).
    *   Add your API keys and database IDs to this file. Example:
        ```env
        NOTION_TOKEN="your_notion_token"
        ANTHROPIC_API_KEY="your_anthropic_key"
        MODEL_NAME="claude-3-opus-20240229" # Or your preferred model
        TIMELINE_DATABASE_ID="your_timeline_db_id"
        LOCATION_DATABASE_ID="your_location_db_id"
        # Add other DB IDs as needed (REGION_DATABASE_ID, etc.)
        ```
    *   Ensure this `.env` file is listed in your `.gitignore` to prevent committing secrets.
    *   The application (`src/backend/constants.py`) uses `python-dotenv` to load these variables.
6.  **Run the Streamlit Application:**
    ```bash
    streamlit run src/app.py
    ```

**Method 2: Dockerized Execution (using Docker and Docker Compose)**

This method uses the provided `Dockerfile` and `docker-compose.yml` to run the application in a containerized environment.

1.  **Prerequisites:**
    *   [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine/CLI installed and running.
2.  **Clone the repository:** (If not already done)
    ```bash
    git clone <repository_url>
    cd kautos-creation
    ```
3.  **Configure Constants via `.env` file:** 
    *   Ensure you have a `.env` file in the project root directory as described in Step 5 of "Method 1: Local Development". The `docker-compose.yml` is configured to use this file to pass environment variables to the container.
4.  **Build and Run with Docker Compose:**
    *   From the project root directory (where `docker-compose.yml` is located), run:
        ```bash
        docker compose up --build -d
        ```
    *   `--build`: Forces Docker Compose to rebuild the Docker image. You can omit `--build` on subsequent runs if the `Dockerfile` or application code (that's copied into the image) hasn't changed.
    *   The application will be accessible at `http://localhost:8501` in your browser.
5.  **Stopping the Application:**
    *   Press `Ctrl+C` in the terminal where `docker compose up` is running.
    *   To remove the containers and networks created by `docker compose up`, run:
        ```bash
        docker compose down
        ```

**Note on Dependencies:** All primary Python dependencies are listed in `pyproject.toml` and managed by `uv sync` (for local development) or within the Docker image build process.