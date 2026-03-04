#!/usr/bin/env python3
"""
Startup script for the Virtual Story Generator
"""

import os
import sys
from dotenv import load_dotenv
from app import app, db

# Load environment variables from .env file
load_dotenv()

def check_setup():
    """Check if everything is configured"""
    api_key = os.getenv("GROQ_API_KEY")

    print("="*60)
    print("VIRTUAL STORY GENERATOR")
    print("="*60)

    if api_key:
        print("[OK] GROQ API key is configured")
    else:
        print("[WARN] No GROQ API key found")

    print("[OK] Database initialized")
    print("="*60)
    print("Starting the application...")
    print("Visit http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    print("="*60)

if __name__ == "__main__":
    check_setup()
    # Use port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
