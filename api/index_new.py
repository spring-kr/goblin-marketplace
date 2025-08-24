# Vercel serverless function - import from root
import sys
import os

# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main app from root index.py
from index import app

# Export for Vercel
application = app

if __name__ == "__main__":
    app.run(debug=True)
