"""
Main entry point for the Note Taking App.
This script runs the Flask application from the backend folder.
"""
import sys
import os

# Add backend folder to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import and run the app
from app import app, init_db

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run the Flask development server
    print("\n" + "="*50)
    print("🚀 Note Taking App is starting...")
    print("="*50)
    print("📂 Backend: backend/app.py")
    print("🎨 Frontend: frontend/templates & frontend/static")
    print("💾 Database: database/notes.db")
    print("="*50)
    print("🌐 Open your browser at: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True)
