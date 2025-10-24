# 📝 Note Taking App

COMP5421 Lab2 exercise: Create a notetaking app and deploy it to Vercel

A full-stack web application built with Flask, SQLite, HTML, CSS, and JavaScript for managing personal notes with CRUD (Create, Read, Update, Delete) functionality.

## 🏗️ Architecture Overview

```
Frontend (HTML/CSS/JS) ↔ Flask Backend ↔ SQLite Database
```

## ✨ Features

- ✅ Create, view, edit, and delete notes
- ✅ Organize notes with categories
- ✅ Search across title/content/category
- ✅ Responsive design (mobile-friendly)
- ✅ Keyboard shortcuts (Ctrl+K for search, Ctrl+N for new note)
- ✅ Auto-hiding flash messages
- ✅ Character counter in forms
- ✅ Confirmation before deleting
- ✅ Timestamps for creation and updates
- ✅ Clean, modern UI with animations

## 📂 Project Structure

```
Notetaking-App/
├── backend/
│   ├── app.py              # Flask backend server
│   └── README.md           # Backend documentation
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
│   │   └── search.html     # Search results page
│   └── README.md           # Frontend documentation
├── database/
│   ├── notes.db            # SQLite database (auto-generated)
│   └── README.md           # Database documentation
├── run.py                  # Main entry point to run the app
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

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

3. **Run the application:**
   ```bash
   python run.py
   ```
   
   Or alternatively, run directly from the backend folder:
   ```bash
   cd backend
   python app.py
   ```

4. **Open your browser:**
   ```
   http://localhost:5000
   ```

The database (`database/notes.db`) will be automatically created on first run.

## 🎯 Key Technologies

### Backend

- **Flask** - Python web framework for routing, templates, and database operations
- **SQLite** - Lightweight file-based database for data persistence

### Frontend

- **HTML5** - Structure and content
- **CSS3** - Styling with Grid/Flexbox layouts and animations
- **JavaScript** - Client-side interactivity and form validation
- **Jinja2** - Template engine for dynamic HTML rendering

## 📚 Application Components

### 1. Backend (`backend/app.py`)

The Flask application handles all server-side logic:

#### Database Schema

```python
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display all notes (homepage) |
| `/add` | GET, POST | Show add note form / Save new note |
| `/note/<id>` | GET | View a specific note |
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
