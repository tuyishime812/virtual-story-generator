#!/usr/bin/env python3
"""
Script to create the first admin user
Run this after the database is initialized
"""

import os
from dotenv import load_dotenv
from app import app, db
from models import User

load_dotenv()

def create_admin():
    """Create the first admin user"""
    
    print("="*60)
    print("CREATE ADMIN USER")
    print("="*60)
    
    with app.app_context():
        # Check if there are any users
        users_count = User.query.count()
        
        if users_count == 0:
            print("\nNo users found in the database.")
            print("Please register a user first, then run this script again.")
            print("\nAlternatively, you can create a user directly here:\n")
            
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            
            if not username or not email or not password:
                print("Error: All fields are required!")
                return
            
            # Create the user
            user = User(username=username, email=email, is_admin=True)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            print(f"\n✓ Admin user '{username}' created successfully!")
            print(f"  Email: {email}")
            print(f"  Role: Administrator")
            print("\nYou can now login and access the admin dashboard at /admin")
        else:
            # Show existing users
            print(f"\nFound {users_count} user(s):\n")
            users = User.query.all()
            
            for i, user in enumerate(users, 1):
                admin_status = "✓ Admin" if user.is_admin else "User"
                print(f"  {i}. {user.username} ({user.email}) - {admin_status}")
            
            # Ask which user to make admin
            print("\nEnter the number of the user to make admin (or 0 to create new): ")
            
            try:
                choice = int(input("> ").strip())
                
                if choice == 0:
                    username = input("Enter new username: ").strip()
                    email = input("Enter new email: ").strip()
                    password = input("Enter password: ").strip()
                    
                    if User.query.filter_by(username=username).first():
                        print("Error: Username already exists!")
                        return
                    if User.query.filter_by(email=email).first():
                        print("Error: Email already exists!")
                        return
                    
                    user = User(username=username, email=email, is_admin=True)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
                    
                    print(f"\n✓ Admin user '{username}' created successfully!")
                elif 1 <= choice <= len(users):
                    user = users[choice - 1]
                    if user.is_admin:
                        print(f"\n✓ User '{user.username}' is already an admin!")
                    else:
                        user.is_admin = True
                        db.session.commit()
                        print(f"\n✓ User '{user.username}' is now an administrator!")
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    create_admin()
