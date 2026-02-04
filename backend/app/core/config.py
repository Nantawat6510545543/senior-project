import os

# Loading .env
DATA_ROOT = os.getenv("DATA_ROOT")

if not DATA_ROOT:
    raise RuntimeError("DATA_ROOT is not set in .env")