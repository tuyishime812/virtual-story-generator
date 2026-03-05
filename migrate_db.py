#!/usr/bin/env python3
"""
Database migration script to add new columns for admin dashboard
"""

import os
from dotenv import load_dotenv
from app import app, db
from sqlalchemy import text

load_dotenv()

def migrate_database():
    """Add new columns to existing database"""
    
    print("="*60)
    print("DATABASE MIGRATION")
    print("="*60)
    
    with app.app_context():
        # Get database connection
        conn = db.engine.connect()
        
        print("\nMigrating users table...")
        
        # Add is_admin column if not exists
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
            print("  [OK] Added is_admin column")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("  [OK] is_admin column already exists")
            else:
                print(f"  [!] is_admin column status unknown: {e}")
        
        # Add is_active_flag column if not exists
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active_flag BOOLEAN DEFAULT 1"))
            print("  [OK] Added is_active_flag column")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("  [OK] is_active_flag column already exists")
            else:
                print(f"  [!] is_active_flag column status unknown: {e}")
        
        # Add last_login column if not exists
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN last_login DATETIME"))
            print("  [OK] Added last_login column")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("  [OK] last_login column already exists")
            else:
                print(f"  [!] last_login column status unknown: {e}")
        
        conn.commit()
        
        print("\nCreating site_visits table...")
        
        # Create site_visits table
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS site_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address VARCHAR(45),
                    user_agent VARCHAR(500),
                    page VARCHAR(200),
                    user_id INTEGER,
                    visited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    referrer VARCHAR(500),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            print("  [OK] Created site_visits table")
        except Exception as e:
            print(f"  [!] site_visits table status unknown: {e}")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("Migration completed successfully!")
        print("="*60)
        print("\nNow run 'python create_admin.py' to create an admin user.")


if __name__ == "__main__":
    migrate_database()
