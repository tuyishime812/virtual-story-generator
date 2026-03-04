"""
WSGI entry point for the Virtual Story Generator
Used by Render and other WSGI-compatible servers
"""

from app import app

if __name__ == "__main__":
    app.run()
