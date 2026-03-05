#!/usr/bin/env python3
"""
Script to create the first admin user - Auto mode
Automatically promotes the first user to admin
"""

import sys
import os
from dotenv import load_dotenv
from app import app, db
from models import User

load_dotenv()

def create_admin_auto():
    """Create or promote a user to admin automatically"""
    
    print("="*60)
    print("CREATE ADMIN USER")
    print("="*60)
    
    with app.app_context():
        # Check if there are any users
        users = User.query.all()
        
        if len(users) == 0:
            print("\nNo users found. Creating default admin user...")
            
            # Create default admin
            admin = User(
                username="admin",
                email="admin@example.com",
                is_admin=True
            )
            admin.set_password("admin123")
            
            db.session.add(admin)
            db.session.commit()
            
            print("\n[OK] Default admin user created!")
            print("  Username: admin")
            print("  Email: admin@example.com")
            print("  Password: admin123")
            print("\n[WARNING] Please change the password after login!")
        else:
            # Check if any admin exists
            admins = User.query.filter_by(is_admin=True).all()
            
            if admins:
                print(f"\n[OK] Found {len(admins)} admin user(s):")
                for admin in admins:
                    print(f"  - {admin.username} ({admin.email})")
                print("\nNo action needed.")
            else:
                # Promote first user to admin
                first_user = users[0]
                first_user.is_admin = True
                db.session.commit()
                
                print(f"\n[OK] Promoted '{first_user.username}' to admin!")
                print(f"  Email: {first_user.email}")
    
    print("\n" + "="*60)
    print("Admin setup complete!")
    print("Visit /admin to access the dashboard")
    print("="*60)


if __name__ == "__main__":
    create_admin_auto()
