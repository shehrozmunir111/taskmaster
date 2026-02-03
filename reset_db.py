from app.db.connection import engine, Base
from app.models.user import User
from app.models.task import Task
from app.models.board import Board, Lane

def reset_database():
    print("Dropping all tables...")
    # Drop all tables in dependency order
    Base.metadata.drop_all(bind=engine)
    
    print("Recreating all tables...")
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database reset complete! All tables have been recreated with the latest schema.")

if __name__ == "__main__":
    reset_database()
