"""
Main entry point for the Note Taking App.
This script runs the Flask application from the backend folder.
Compatible with both local development and Vercel deployment.
"""
import sys
import os

# Add backend folder to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import and run the app
from app import app, init_db

# Initialize database (for local development)
# On Vercel, make sure table is created in Supabase first
try:
    init_db()
except Exception as e:
    print(f"Note: Database initialization skipped - {e}")

# For Vercel serverless deployment
# Vercel will use this 'app' object
app = app

if __name__ == '__main__':
    # Run the Flask development server (local only)
    print("\n" + "="*50)
    print("🚀 Note Taking App is starting...")
    print("="*50)
    print("📂 Backend: backend/app.py")
    print("🎨 Frontend: frontend/templates & frontend/static")
    print("💾 Database: Supabase PostgreSQL")
    print("="*50)
    print("🌐 Open your browser at: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True)
