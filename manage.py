#!/usr/bin/env python
"""
TaskMaster Management CLI

Professional administrative utility for managing the TaskMaster application.
Usage:
    python manage.py init-db        - Reset and initialize database tables
    python manage.py create-admin   - Create a new administrative user
"""

import sys
import argparse
import getpass
from sqlalchemy.orm import Session

from app.db.connection import engine, Base, SessionLocal
from app.models.user import User
from app.core.security import hash_password
# Import all models to ensure metadata is loaded
from app.models.task import Task
from app.models.board import Board, Lane

def init_db():
    """Drops and recreates all database tables."""
    print("Initializing Database...")
    print("   - Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("   - Creating new schema...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

def create_admin():
    """Interactively creates a system administrator."""
    print("Create Admin User")
    print("-------------------")
    
    db = SessionLocal()
    try:
        email = input("Email: ").strip()
        if not email:
            print("Email is required.")
            return

        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User {email} already exists.")
            update = input("Do you want to promote them to admin? (y/n): ").lower()
            if update == 'y':
                existing_user.role = "admin"
                db.commit()
                print(f"User {email} promoted to Admin.")
            return

        full_name = input("Full Name: ").strip()
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")

        if password != confirm_password:
            print("Passwords do not match.")
            return

        print("   - Hashing password...")
        hashed_pwd = hash_password(password)
        
        new_admin = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_pwd,
            role="admin",  # Explicitly set role
            is_active=True
        )
        
        db.add(new_admin)
        db.commit()
        print(f"Admin user {email} created successfully.")
        
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="TaskMaster Management CLI")
    parser.add_argument('command', choices=['init-db', 'create-admin'], help="Command to execute")
    parser.add_argument('--email', help="Admin email for non-interactive creation")
    parser.add_argument('--password', help="Admin password for non-interactive creation")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if args.command == 'init-db':
        confirm = input("This will DELETE ALL DATA. Are you sure? (y/n): ")
        if confirm.lower() == 'y':
            init_db()
        else:
            print("Operation cancelled.")
            
    if args.command == 'create-admin':
        if args.email and args.password:
            # Non-interactive mode
            db = SessionLocal()
            try:
                hashed_pwd = hash_password(args.password)
                new_admin = User(
                    email=args.email,
                    full_name="System Admin",
                    hashed_password=hashed_pwd,
                    role="admin",
                    is_active=True
                )
                db.add(new_admin)
                db.commit()
                print(f"Admin user {args.email} created successfully (Non-interactive).")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                db.close()
        else:
            create_admin()

if __name__ == "__main__":
    main()
