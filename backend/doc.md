# Backend - Flask Application

This folder contains the Flask backend server code.

## Files

- `app.py` - Main Flask application with routes and database logic

## Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display all notes (homepage) |
| `/add` | GET, POST | Show add note form / Save new note |
| `/note/<id>` | GET | View a specific note |
| `/edit/<id>` | GET, POST | Show edit form / Update note |
| `/delete/<id>` | POST | Delete a note |
| `/search` | GET | Search notes by keywords |
| `/api/notes` | GET | API endpoint returning JSON data |

## Configuration

The Flask app is configured to use:
- Templates from: `../frontend/templates/`
- Static files from: `../frontend/static/`
- Database from: `../database/notes.db`

## Running

Use the main `run.py` script from the project root:
```bash
python run.py
```
