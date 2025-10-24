"""
Initialize Supabase PostgreSQL Database using Supabase Client SDK
This script creates the notes table in your Supabase PostgreSQL database.
Run this once before starting your application.
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_supabase_db():
    """Initialize the Supabase database with the notes table using SQL via RPC"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env file")
        print("\n📝 Please update your .env file with:")
        print("   SUPABASE_URL=https://your-project.supabase.co")
        print("   SUPABASE_KEY=your-anon-key")
        return False
    
    try:
        print("Connecting to Supabase...")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        print("\n⚠️  Note: Table creation requires SQL Editor access in Supabase Dashboard")
        print("=" * 70)
        print("\n📋 Please run the following SQL in your Supabase SQL Editor:")
        print("   (Dashboard → SQL Editor → New Query)")
        print("\n" + "-" * 70)
        
        sql_script = """
-- Create notes table
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    tags TEXT,
    event_date DATE,
    event_time TIME,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_notes_updated_at ON notes(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_notes_event_date ON notes(event_date DESC);
CREATE INDEX IF NOT EXISTS idx_notes_created_at ON notes(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notes_title ON notes(title);

-- Enable Row Level Security (optional, for future use)
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (for development)
-- You can customize this later for user-specific access
DROP POLICY IF EXISTS "Allow all operations for notes" ON notes;
CREATE POLICY "Allow all operations for notes" 
ON notes FOR ALL 
USING (true) 
WITH CHECK (true);
"""
        
        print(sql_script)
        print("-" * 70)
        print("\n✅ After running the SQL above, your database will be ready!")
        print("\n🔍 To verify, check: Dashboard → Table Editor → 'notes' table")
        
        # Try to check if table exists
        try:
            test_query = supabase.table('notes').select('id').limit(1).execute()
            print("\n✓ Connection successful! Table 'notes' detected.")
            print("✓ Database is ready to use!")
            return True
        except Exception as e:
            print(f"\n⚠️  Table not found yet. Please run the SQL script above.")
            print(f"   Details: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Tips:")
        print("   1. Check your SUPABASE_URL format: https://xxxxx.supabase.co")
        print("   2. Check your SUPABASE_KEY (should be the 'anon' public key)")
        print("   3. Make sure your Supabase project is active")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Supabase Database Initialization (Using Supabase Client SDK)")
    print("=" * 70)
    init_supabase_db()
