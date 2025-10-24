# Project Structure

## 📁 Folder Organization

The project has been restructured into three main components for better organization and separation of concerns:

```
Notetaking-App/
│
├── 🔧 backend/              # Backend server code
│   ├── app.py              # Flask application & routes
│   └── README.md           # Backend documentation
│
├── 🎨 frontend/             # User interface files
│   ├── static/             # CSS, JavaScript, images
│   │   ├── style.css       # Application styling
│   │   └── script.js       # Client interactions
│   ├── templates/          # HTML templates (Jinja2)
│   │   ├── base.html       # Master template
│   │   ├── index.html      # Homepage
│   │   ├── add_note.html   # Create note form
│   │   ├── edit_note.html  # Edit note form
│   │   ├── view_note.html  # View note page
│   │   └── search.html     # Search results
│   └── README.md           # Frontend documentation
│
├── 💾 database/             # Database storage
│   ├── notes.db            # SQLite database (auto-generated)
│   └── README.md           # Database documentation
│
├── 🚀 run.py               # Main entry point
├── 📋 requirements.txt     # Python dependencies
├── 📖 README.md            # Main documentation
└── 🚫 .gitignore           # Git ignore rules
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Browser                         │
│                   (HTML/CSS/JS)                          │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP Requests
                 ↓
┌─────────────────────────────────────────────────────────┐
│              Flask Backend (backend/app.py)              │
│  • Routes & Controllers                                  │
│  • Business Logic                                        │
│  • Template Rendering                                    │
└────────────────┬────────────────────────────────────────┘
                 │ SQL Queries
                 ↓
┌─────────────────────────────────────────────────────────┐
│           SQLite Database (database/notes.db)            │
│  • Notes Table (id, title, content, category, dates)    │
└─────────────────────────────────────────────────────────┘
```

## 📂 Separation of Concerns

### Backend (`backend/`)
- **Purpose**: Server-side logic and API endpoints
- **Technologies**: Python, Flask, SQLite
- **Responsibilities**:
  - Handle HTTP requests/responses
  - Database operations (CRUD)
  - Business logic
  - Route definitions
  - Template rendering

### Frontend (`frontend/`)
- **Purpose**: User interface and client-side logic
- **Technologies**: HTML, CSS, JavaScript, Jinja2
- **Responsibilities**:
  - UI layout and design
  - User interactions
  - Form validation
  - Animations and effects
  - Template structure

### Database (`database/`)
- **Purpose**: Data persistence
- **Technologies**: SQLite
- **Responsibilities**:
  - Store notes data
  - Maintain data integrity
  - Handle queries

## 🚀 Running the Application

### Option 1: Using run.py (Recommended)
```bash
python run.py
```

### Option 2: Direct backend execution
```bash
cd backend
python app.py
```

## 🔄 Data Flow

1. **User Request** → Browser sends HTTP request
2. **Routing** → Flask backend receives and routes request
3. **Processing** → Backend processes logic and queries database
4. **Database** → SQLite returns data
5. **Rendering** → Backend renders template with data
6. **Response** → HTML/CSS/JS sent back to browser
7. **Display** → User sees the page

## 📝 File Relationships

```
run.py
  ↓ imports
backend/app.py
  ↓ uses
frontend/templates/*.html  (Jinja2 templates)
  ↓ includes
frontend/static/style.css  (styling)
frontend/static/script.js  (interactivity)
  ↓ reads/writes
database/notes.db  (data storage)
```

## 🎯 Benefits of This Structure

✅ **Clear Separation**: Frontend, backend, and database are clearly separated
✅ **Easy Navigation**: Developers can quickly find relevant files
✅ **Scalability**: Easy to add new features in the right place
✅ **Maintainability**: Changes to one component don't affect others
✅ **Team Collaboration**: Multiple developers can work on different parts
✅ **Version Control**: Better organization for Git commits
✅ **Deployment**: Easier to deploy different components separately

## 🔧 Configuration

The Flask app in `backend/app.py` is configured to find resources:

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'frontend', 'static'))

DATABASE = os.path.join(BASE_DIR, 'database', 'notes.db')
```

This ensures all paths are relative to the project root, regardless of where the script is run from.
