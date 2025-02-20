import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the database URL from environment variables,
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
