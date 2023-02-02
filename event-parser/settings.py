import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load environments from environment file
# , '.env'
load_dotenv(BASE_DIR.parent / os.getenv('DOT_ENV_FILENAME'))

DATABASE_CONNECTION = f"postgresql://" \
                      f"{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST', 'localhost')}:" \
                      f"{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"

# Time for start event schedule harvest
UGRA_CLASSIC_HARVEST_TIME = os.getenv('UGRA_CLASSIC_HARVEST_TIME', default="02:00")
