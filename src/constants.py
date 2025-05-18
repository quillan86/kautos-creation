import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from root directory
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")

TIMELINE_DATABASE_ID = "1f6c1f3a9cd0807a8d37fea4cf41c9de"
LOCATION_DATABASE_ID = "1f6c1f3a9cd080e1a7f0d913e6919011"
REGION_DATABASE_ID = "1f6c1f3a9cd080c19d61cface2b4ee09"
POLITY_DATABASE_ID = "1f6c1f3a9cd0805e8847f3fe1a5ec43d"
LANGUAGE_DATABASE_ID = "1f6c1f3a9cd080f19b39f5934d1614f2"
RELIGION_DATABASE_ID = "1f7c1f3a9cd080bc8064c085f79e5446"
