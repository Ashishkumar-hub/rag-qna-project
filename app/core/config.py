import os
from dotenv import load_dotenv

# Load environment variables from the correct path
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "configs", ".env"
)
load_dotenv(dotenv_path)

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
