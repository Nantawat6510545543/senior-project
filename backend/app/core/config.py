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


# Check path exists
if not os.path.exists(DATA_ROOT):
    raise RuntimeError(
        f"DATA_ROOT does not exist or is not accessible: {DATA_ROOT}\n\n"
        "Common causes:\n"
        "- Network drive (e.g., Z:) is not mounted\n"
        "- Docker cannot access the drive\n"
        "- Path is incorrect\n"
    )

# Check path is not empty
if not os.listdir(DATA_ROOT):
    raise RuntimeError(
        f"DATA_ROOT exists but is empty: {DATA_ROOT}\n\n"
        "This usually indicates a failed volume mount.\n"
        "Fix:\n"
        "- Ensure dataset is mounted on host\n"
        "- Verify with: docker exec -it <container> ls /dataset"
    )