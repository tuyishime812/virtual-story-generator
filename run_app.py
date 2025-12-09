#!/usr/bin/env python3
"""
Startup script for the Virtual Story Generator
"""

import os
import sys
from app import app

def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("GEMINI_API_KEY")

    print("="*60)
    print("VIRTUAL STORY GENERATOR")
    print("="*60)

    if api_key:
        print("✓ API key is configured - you'll get full stories!")
    else:
        print("⚠️  No API key found - using demo mode with sample stories")
        print("\nTo generate full, rich stories:")
        print("1. Get your Gemini API key from Google AI Studio")
        print("2. Create a .env file in this directory")
        print("3. Add: GEMINI_API_KEY=your_actual_api_key_here")
        print("4. Restart the application")

    print("="*60)
    print("Starting the application...")
    print("Visit http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    print("="*60)

if __name__ == "__main__":
    check_api_key()
    # Use port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)