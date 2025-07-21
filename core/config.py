# config.py

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Paths to key files
APP_USAGE_LOG = BASE_DIR / "data" / "app_usage_log.csv"
BURNOUT_LOG = BASE_DIR / "data" / "burnout_log.csv"
FEEDBACK_LOG = BASE_DIR / "data" / "feedback_log.csv"
GOALS_LOG = BASE_DIR / "data" / "goals_log.csv"
SELF_ASSESSMENT_LOG = BASE_DIR / "data" / "self_assessment_log.csv"

# Create 'data' folder if it doesn't exist
os.makedirs(BASE_DIR / "data", exist_ok=True)