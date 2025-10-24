"""
Database Migration Script
Adds tags, event_date, and event_time fields to existing notes table
"""
import sqlite3
import os

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'notes.db')

def migrate_database():
    """Add new columns to existing notes table"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(notes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add tags column if it doesn't exist
        if 'tags' not in columns:
            print("Adding 'tags' column...")
            cursor.execute("ALTER TABLE notes ADD COLUMN tags TEXT")
            print("✓ 'tags' column added")
        else:
            print("✓ 'tags' column already exists")
        
        # Add event_date column if it doesn't exist
        if 'event_date' not in columns:
            print("Adding 'event_date' column...")
            cursor.execute("ALTER TABLE notes ADD COLUMN event_date DATE")
            print("✓ 'event_date' column added")
        else:
            print("✓ 'event_date' column already exists")
        
        # Add event_time column if it doesn't exist
        if 'event_time' not in columns:
            print("Adding 'event_time' column...")
            cursor.execute("ALTER TABLE notes ADD COLUMN event_time TIME")
            print("✓ 'event_time' column added")
        else:
            print("✓ 'event_time' column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"\n❌ Error during migration: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("="*50)
    print("Note Taking App - Database Migration")
    print("="*50)
    print(f"Database: {DATABASE}\n")
    
    if not os.path.exists(DATABASE):
        print("❌ Database file not found!")
        print("Please run the app first to create the database.")
    else:
        migrate_database()
    
    print("="*50)
