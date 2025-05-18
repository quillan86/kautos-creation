import os
from dotenv import load_dotenv

# Attempt to load .env file for local development (outside Docker)
# In Docker, Docker Compose's `env_file` directive should set these.
# load_dotenv() will not override existing environment variables.
load_dotenv() 

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-7-sonnet-20250219")

TIMELINE_DATABASE_ID = os.getenv("TIMELINE_DATABASE_ID")
LOCATION_DATABASE_ID = os.getenv("LOCATION_DATABASE_ID")
REGION_DATABASE_ID = os.getenv("REGION_DATABASE_ID")
POLITY_DATABASE_ID = os.getenv("POLITY_DATABASE_ID")
LANGUAGE_DATABASE_ID = os.getenv("LANGUAGE_DATABASE_ID")
RELIGION_DATABASE_ID = os.getenv("RELIGION_DATABASE_ID")

# Warnings for missing critical variables
if NOTION_TOKEN is None:
    print("CRITICAL WARNING: NOTION_TOKEN not found. Application may not function correctly.")
if ANTHROPIC_API_KEY is None:
    print("CRITICAL WARNING: ANTHROPIC_API_KEY not found. Application may not function correctly.")
if TIMELINE_DATABASE_ID is None:
    print("WARNING: TIMELINE_DATABASE_ID not found.")
if LOCATION_DATABASE_ID is None:
    print("WARNING: LOCATION_DATABASE_ID not found.")

# You can add more checks for other database IDs if they are critical
