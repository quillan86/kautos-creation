import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from root directory
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-3-7-sonnet-20250219"

TIMELINE_DATABASE_ID = os.getenv("TIMELINE_DATABASE_ID")
LOCATION_DATABASE_ID = os.getenv("LOCATION_DATABASE_ID")
REGION_DATABASE_ID = os.getenv("REGION_DATABASE_ID")
POLITY_DATABASE_ID = os.getenv("POLITY_DATABASE_ID")
LANGUAGE_DATABASE_ID = os.getenv("LANGUAGE_DATABASE_ID")
RELIGION_DATABASE_ID = os.getenv("RELIGION_DATABASE_ID")

# Ensure you have placeholder/actual values for database IDs if not in .env
if NOTION_TOKEN is None:
    print("Warning: NOTION_TOKEN not found. Please set it in your .env file or environment variables.")
if ANTHROPIC_API_KEY is None:
    print("Warning: ANTHROPIC_API_KEY not found. Please set it in your .env file or environment variables.")
