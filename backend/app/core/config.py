"""Load .env file"""
import os

# Load variables
DATA_ROOT = os.getenv("DATA_ROOT")
FRONTEND_URL = os.getenv("FRONTEND_URL")
BACKEND_URL = os.getenv("BACKEND_URL")

# Check that they are set
if not DATA_ROOT:
    raise RuntimeError("DATA_ROOT is not set in .env")
if not FRONTEND_URL:
    raise RuntimeError("FRONTEND_URL is not set in .env")
if not BACKEND_URL:
    raise RuntimeError("BACKEND_URL is not set in .env")
