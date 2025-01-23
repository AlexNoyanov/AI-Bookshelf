import os
import sys
from dotenv import load_dotenv

# Get the absolute path to the project root
current_dir = os.path.dirname(os.path.abspath(__file__))  # tests directory
project_root = os.path.dirname(current_dir)  # go up one level
print("Project root path: {}".format(project_root))  # Debug print

# Add the project root to Python path
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))

try:
    from utils.db import Database
    print("Successfully imported Database class")
except ImportError as e:
    print("Import error: {}".format(e))
    print("Python path: {}".format(sys.path))
    sys.exit(1)

def test_db():
    db = Database()
    db.test_connection()

if __name__ == "__main__":
    test_db()
