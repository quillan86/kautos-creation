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
