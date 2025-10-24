# 📝 Note Taking App

COMP5421 Lab2 exercise: Create a notetaking app and deploy it to Vercel

A full-stack web application built with Flask, Supabase PostgreSQL, HTML, CSS, and JavaScript for managing personal notes with CRUD (Create, Read, Update, Delete) functionality and AI-powered features.

## 🏗️ Architecture Overview

```
Frontend (HTML/CSS/JS) ↔ Flask Backend ↔ Supabase PostgreSQL Database
                              ↓
                    OpenAI/GitHub Models API
```

## ✨ Features

### Core Features
- ✅ Create, view, edit, and delete notes
- ✅ Organize notes with categories and tags
- ✅ Search across title/content/category/tags
- ✅ Event date and time tracking
- ✅ Multiple sorting options (updated, created, event date, title)
- ✅ Responsive design (mobile-friendly)
- ✅ Keyboard shortcuts (Ctrl+K for search, Ctrl+N for new note)
- ✅ Auto-hiding flash messages
- ✅ Character counter in forms
- ✅ Confirmation before deleting
- ✅ Timestamps for creation and updates
- ✅ Clean, modern UI with animations

### AI-Powered Features 🤖
- ✅ **Smart Note Generation**: Convert natural language to structured notes
- ✅ **Multi-language Translation**: Translate notes to 10 languages
- ✅ **Auto-tagging**: Generate relevant tags from content
- ✅ **Note Summarization**: Create concise summaries
- ✅ **Date/Time Extraction**: Automatically parse dates and times from text

## 📂 Project Structure

```
Notetaking-App/
├── backend/
│   ├── app.py              # Flask backend server with routes
│   ├── llm.py              # LLM integration (OpenAI/GitHub Models)
│   └── doc.md              # Backend documentation
├── frontend/
│   ├── static/
│   │   ├── style.css       # CSS styling
│   │   └── script.js       # JavaScript interactions
│   ├── templates/
│   │   ├── base.html       # Base template (master layout)
│   │   ├── index.html      # Homepage (all notes)
│   │   ├── add_note.html   # Create new note form
│   │   ├── edit_note.html  # Edit existing note form
│   │   ├── view_note.html  # View single note
│   │   ├── generate_note.html  # AI note generation
│   │   └── search.html     # Search results page
│   └── doc.md              # Frontend documentation
├── database/
│   └── doc.md              # Database documentation
├── init_supabase.py        # Database initialization script
├── run.py                  # Main entry point to run the app
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── STRUCTURE.md            # Architecture documentation
├── MIGRATION_GUIDE.md      # SQLite to PostgreSQL migration guide
└── API_DOCUMENTATION.md    # API endpoints documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Supabase account (free tier available)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yausum/Notetaking-App.git
   cd Notetaking-App
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Supabase:**
   - Create a project at [Supabase](https://supabase.com)
   - Get your database connection string from Project Settings > Database
   - Copy the "Connection pooling" URI (Transaction mode)

4. **Configure environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   # GitHub Models API (for AI features)
   GITHUB_TOKEN=your_github_token_here
   OPENAI_MODEL=openai/gpt-4.1-mini
   
   # Supabase PostgreSQL
   DATABASE_URL=postgresql://postgres.xxxxx:password@host:6543/postgres
   ```

5. **Initialize the database:**
   ```bash
   python init_supabase.py
   ```
   
   This will create the `notes` table and indexes in your Supabase database.

6. **Run the application:**
   ```bash
   python run.py
   ```
   
   Or alternatively, run directly from the backend folder:
   ```bash
   cd backend
   python app.py
   ```

7. **Open your browser:**
   ```
   http://localhost:5000
   ```

### Migration from SQLite

If you're upgrading from the SQLite version, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions.

## 🎯 Key Technologies

### Backend

- **Flask 3.0.0** - Python web framework for routing, templates, and database operations
- **PostgreSQL (Supabase)** - Cloud-hosted relational database with real-time capabilities
- **psycopg2** - PostgreSQL adapter for Python
- **OpenAI API** - AI-powered note generation and translation

### Frontend

- **HTML5** - Structure and content
- **CSS3** - Styling with Grid/Flexbox layouts and animations
- **JavaScript (ES6+)** - Client-side interactivity, async/await API calls
- **Jinja2** - Template engine for dynamic HTML rendering

### AI Integration

- **GitHub Models** - Access to OpenAI GPT-4 models
- **OpenAI SDK** - Python client for API calls

## 📚 Application Components

### 1. Backend (`backend/app.py`)

The Flask application handles all server-side logic:

#### Database Schema

```sql
CREATE TABLE notes (
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
```

#### Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display all notes (homepage) with sorting |
| `/add` | GET, POST | Show add note form / Save new note |
| `/generate` | GET | AI-powered note generation interface |
| `/note/<id>` | GET | View a specific note |
| `/edit/<id>` | GET, POST | Edit form / Update note |
| `/delete/<id>` | POST | Delete a note |
| `/search` | GET | Search notes by query |
| `/api/notes` | GET | JSON API for all notes |
| `/api/translate` | POST | Translate note content |
| `/api/generate-note` | POST | Generate structured note from text |
| `/api/generate-tags` | POST | Auto-generate tags |
| `/api/summarize` | POST | Summarize note content |
| `/edit/<id>` | GET, POST | Show edit form / Update note |
| `/delete/<id>` | POST | Delete a note |
| `/search` | GET | Search notes by keywords |
| `/api/notes` | GET | API endpoint returning JSON data |

### 2. Templates (`frontend/templates/`)

#### `base.html` - Master Template

Provides the common layout for all pages:
- Navigation bar with logo and links
- Global search bar
- Flash message container
- Content block (overridden by child templates)
- Footer

**Template Inheritance:**
```html
<!-- Child templates extend base.html -->
{% extends "base.html" %}

<!-- Override title block -->
{% block title %}My Custom Title{% endblock %}

<!-- Override content block -->
{% block content %}
  <h1>My Content</h1>
{% endblock %}
```

#### `index.html` - Homepage

Displays all notes in a responsive grid layout:
- Shows note cards with title, category, preview (150 chars), and date
- Action buttons: View, Edit, Delete
- Empty state message when no notes exist

#### `add_note.html` - Create Note

Form with three fields:
- Title (required)
- Category (optional)
- Content (required, with character counter)

#### `edit_note.html` - Edit Note

Similar to add form but pre-filled with existing note data.

#### `view_note.html` - View Note

Displays complete note details:
- Full title and metadata (category, timestamps)
- Complete content with preserved line breaks
- Edit and Delete action buttons

#### `search.html` - Search Results

Shows notes matching the search query:
- Searches across title, content, and category fields
- Displays results count
- Empty state for no results

### 3. Styling (`frontend/static/style.css`)

**Design System:**
- CSS custom properties for consistent colors
- Responsive grid layout (auto-adjusts columns)
- Card-based UI with hover effects
- Smooth transitions and animations

**Key Features:**
```css
/* Responsive grid */
.notes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

/* Card hover effect */
.note-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Mobile responsive */
@media (max-width: 768px) {
    .notes-grid {
        grid-template-columns: 1fr;
    }
}
```

### 4. JavaScript (`frontend/static/script.js`)

Client-side interactivity:

**Auto-hide Flash Messages:**
```javascript
// Fade out after 5 seconds
setTimeout(() => {
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 500);
}, 5000);
```

**Keyboard Shortcuts:**
- `Ctrl+K` / `Cmd+K` - Focus search bar
- `Ctrl+N` / `Cmd+N` - Create new note

**Form Validation:**
- Validates title and content before submission
- Real-time character counting

**Search Animation:**
- Subtle scale effect on focus

## 🔄 Data Flow Example: Creating a Note

1. **User clicks "New Note"** → Browser navigates to `/add`

2. **Server responds** → Renders `add_note.html` form

3. **User fills form and submits** → Browser sends POST request

4. **Server processes:**
   ```python
   title = request.form['title']
   content = request.form['content']
   conn.execute('INSERT INTO notes (...) VALUES (?, ?, ?)', (...))
   flash('Note added successfully!')
   return redirect(url_for('index'))
   ```

5. **User redirected to homepage** → New note appears in grid

## 🔍 Search Functionality

The search feature uses SQL LIKE queries to find matches:

```python
notes = conn.execute(
    '''SELECT * FROM notes 
       WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
       ORDER BY updated_at DESC''',
    (f'%{query}%', f'%{query}%', f'%{query}%')
).fetchall()
```

Searches in:
- Note titles
- Note content
- Categories

## 🎨 UI/UX Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Card-based Layout** - Clean, modern note cards
- **Hover Effects** - Visual feedback on interactions
- **Flash Messages** - Success/error notifications with auto-hide
- **Empty States** - Helpful messages when no content exists
- **Form Validation** - Prevents invalid submissions
- **Loading Animations** - Smooth transitions throughout

## 📱 Responsive Breakpoints

- **Desktop**: Multi-column grid layout (auto-fit)
- **Tablet**: 2-column layout
- **Mobile** (`<768px`): Single-column layout

## 🛠️ Development

### Folder Structure

- **Backend Logic**: `backend/app.py`
- **Frontend Templates**: `frontend/templates/*.html`
- **Styling**: `frontend/static/style.css`
- **Interactivity**: `frontend/static/script.js`
- **Database**: `database/notes.db` (auto-generated)

### Dependencies

```
Flask==3.0.0
Werkzeug==3.0.1
```

### Debug Mode

The app runs in debug mode by default:
```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

This enables:
- Auto-reload on code changes
- Detailed error pages
- Interactive debugger

## 🚢 Deployment

Deploy to Vercel or any platform supporting Python Flask applications.

## 📄 License

This project is for educational purposes (COMP5421 Lab2).

## 👨‍💻 Author

**yausum**
- GitHub: [@yausum](https://github.com/yausum)

---

Built with Flask, SQLite, and ❤️
