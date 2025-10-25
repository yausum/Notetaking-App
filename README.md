# 📝 Note Taking App

COMP5421 Lab2 exercise: Create a notetaking app and deploy it to Vercel

A full-stack web application built with Flask, Supabase PostgreSQL, HTML, CSS, and JavaScript for managing personal notes with CRUD (Create, Read, Update, Delete) functionality and AI-powered features.

**🌐 Live Demo**: [Deployed on Vercel](https://notetaking-app-weld.vercel.app/)

## 🏗️ Architecture Overview

```
Frontend (HTML/CSS/JS) ↔ Flask Backend (Vercel) ↔ Supabase PostgreSQL Database
                              ↓
                    OpenAI/GitHub Models API
```

### Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Backend**: Flask 3.0.0 (Python)
- **Database**: Supabase PostgreSQL (with Python SDK)
- **AI**: OpenAI GPT-4.1-mini via GitHub Models
- **Deployment**: Vercel (Serverless Functions)

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
- ✅ **Smart Note Generation**: Convert natural language to structured notes with auto-extraction of:
  - Title, content, category
  - Up to 3 relevant tags
  - Event dates and times from natural language (e.g., "tomorrow 5pm", "next Monday")
- ✅ **Multi-language Translation**: Translate notes to 10 languages (English, 中文繁體/简体, 日本語, 한국어, Español, Français, Deutsch, Italiano, Português)
- ✅ **Auto-tagging**: Generate relevant tags from content using AI
- ✅ **Note Summarization**: Create concise summaries
- ✅ **Date/Time Extraction**: Automatically parse dates and times from text
- ✅ **Multi-language Generation**: Generate notes in any supported language

## 📂 Project Structure

```
Notetaking-App/
├── backend/
│   ├── app.py              # Flask backend server with routes
│   ├── llm.py              # LLM integration (OpenAI/GitHub Models)
│   └── doc.md              # Backend documentation
├── frontend/
│   ├── static/
│   │   ├── style.css       # CSS styling (1000+ lines)
│   │   └── script.js       # JavaScript interactions
│   ├── templates/
│   │   ├── base.html       # Base template (master layout)
│   │   ├── index.html      # Homepage (all notes)
│   │   ├── add_note.html   # Create new note form
│   │   ├── edit_note.html  # Edit existing note form
│   │   ├── view_note.html  # View single note
│   │   ├── generate_note.html  # AI note generation with preview
│   │   └── search.html     # Search results page
│   └── doc.md              # Frontend documentation
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot project standards
├── database/
│   └── doc.md              # Database documentation
├── init_supabase.py        # Database initialization script
├── run.py                  # Application entry point (Vercel-compatible)
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── .env                    # Environment variables (not in git)
├── lab2_writeup.md         # Comprehensive project writeup
├── MIGRATION_GUIDE.md      # SQLite to Supabase migration guide
├── SETUP_GUIDE.md          # Setup instructions
├── VERCEL_DEPLOYMENT.md    # Vercel deployment guide
├── STRUCTURE.md            # Architecture documentation
└── API_DOCUMENTATION.md    # API endpoints documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Supabase account (free tier available at [supabase.com](https://supabase.com))
- GitHub account with access to GitHub Models (for AI features)

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
   - Copy your Project URL and anon/public API key from Project Settings > API
   - Run the initialization script to create the database table:
     ```bash
     python init_supabase.py
     ```
   - Copy the SQL output and run it in Supabase SQL Editor (Dashboard > SQL Editor)

4. **Configure environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   # GitHub Models API (for AI features)
   GITHUB_TOKEN=your_github_token_here
   OPENAI_MODEL=gpt-4o-mini
   
   # Supabase PostgreSQL
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_anon_public_key_here
   ```

   **Getting GitHub Token:**
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Generate a new token with appropriate permissions
   - Use this token for AI features via GitHub Models

5. **Run the database initialization:**
   ```bash
   python init_supabase.py
   ```
   
   This will output SQL commands. Copy and paste them into your Supabase SQL Editor to create:
   - `notes` table with proper schema
   - Indexes for optimized queries
   - Row Level Security policies

6. **Run the application:**
   ```bash
   python run.py
   ```
   
   The app will start on `http://localhost:5000`

7. **Open your browser:**
   ```
   http://localhost:5000
   ```

## 🚀 Deployment to Vercel

This app is configured for serverless deployment on Vercel:

1. **Push your code to GitHub**

2. **Import project to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository

3. **Configure environment variables in Vercel:**
   - Add all variables from your `.env` file
   - Go to Project Settings > Environment Variables
   - Add: `GITHUB_TOKEN`, `OPENAI_MODEL`, `SUPABASE_URL`, `SUPABASE_KEY`

4. **Deploy:**
   - Vercel will automatically detect the Flask app
   - Uses `vercel.json` configuration
   - Deploys as serverless functions

5. **Access your live app:**
   - Vercel provides a URL like `your-app.vercel.app`

### Vercel Configuration

The `vercel.json` file configures the deployment:
```json
{
  "builds": [
    {
      "src": "run.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run.py"
    }
  ]
}
```

## 🎯 Key Technologies

### Backend

- **Flask 3.0.0** - Python web framework for routing, templates, and API endpoints
- **Supabase Python SDK 2.10.0** - Cloud PostgreSQL database client with real-time capabilities
- **PostgreSQL** - Robust relational database with advanced features
- **OpenAI API** - AI-powered note generation, translation, and summarization via GitHub Models
- **python-dotenv 1.0.0** - Environment variable management

### Frontend

- **HTML5** - Structure and content with semantic markup
- **CSS3** - Styling with Grid/Flexbox layouts, animations, and responsive design
- **JavaScript (ES6+)** - Client-side interactivity, async/await API calls, DOM manipulation
- **Jinja2** - Template engine for dynamic HTML rendering with template inheritance

### AI Integration

- **GitHub Models** - Access to OpenAI GPT-4 models via GitHub's API
- **OpenAI SDK 1.106.1** - Python client for API calls with streaming support
- **Temperature Control**: 0.3 for structured extraction, 0.7 for creative generation

### Deployment & DevOps

- **Vercel** - Serverless deployment platform with automatic CI/CD
- **Git** - Version control with GitHub integration
- **Environment Variables** - Secure configuration management

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
    tags TEXT,                -- Comma-separated, max 3
    event_date DATE,          -- Optional: YYYY-MM-DD
    event_time TIME,          -- Optional: HH:MM (24-hour)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_notes_updated_at ON notes(updated_at DESC);
CREATE INDEX idx_notes_event_date ON notes(event_date ASC NULLS LAST);
CREATE INDEX idx_notes_created_at ON notes(created_at DESC);
```

**Database Access**: Uses Supabase Python SDK (NOT direct psycopg2):
```python
# Query
response = supabase.table('notes').select('*').eq('id', note_id).execute()
note = response.data[0] if response.data else None

# Insert
response = supabase.table('notes').insert({
    'title': title,
    'content': content
}).execute()

# Update
supabase.table('notes').update({
    'title': title,
    'updated_at': datetime.now().isoformat()
}).eq('id', note_id).execute()

# Delete
supabase.table('notes').delete().eq('id', note_id).execute()
```

#### Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display all notes (homepage) with sorting options |
| `/add` | GET, POST | Show add note form / Save new note |
| `/generate` | GET | AI-powered note generation interface |
| `/note/<id>` | GET | View a specific note with full details |
| `/edit/<id>` | GET, POST | Edit form / Update note |
| `/delete/<id>` | POST | Delete a note (with confirmation) |
| `/search` | GET | Search notes by query (title/content/category/tags) |
| `/api/notes` | GET | JSON API for all notes |
| `/api/translate` | POST | Translate note content to target language |
| `/api/generate-note` | POST | Generate structured note from natural language |
| `/api/generate-tags` | POST | Auto-generate tags from content |
| `/static/<path>` | GET | Serve static files (CSS, JS) - Vercel compatible |

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

The search feature uses Supabase's `ilike` operator for case-insensitive pattern matching:

```python
# Search across multiple fields
search_pattern = f'%{query}%'
response = supabase.table('notes') \
    .select('*') \
    .or_(f'title.ilike.{search_pattern},content.ilike.{search_pattern},category.ilike.{search_pattern},tags.ilike.{search_pattern}') \
    .order('updated_at', desc=True) \
    .execute()
notes = response.data
```

Searches in:
- Note titles
- Note content
- Categories
- Tags

**Case-insensitive** and supports partial matches.

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

### Project Architecture

```
┌─────────────────────────────────────────────────┐
│              User Browser                       │
│  (HTML/CSS/JS - Jinja2 Templates)              │
└─────────────────┬───────────────────────────────┘
                  │ HTTP Requests
                  ▼
┌─────────────────────────────────────────────────┐
│         Flask Application (run.py)              │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Routes & Controllers (app.py)           │  │
│  │  - CRUD operations                       │  │
│  │  - API endpoints                         │  │
│  │  - Template rendering                    │  │
│  └────────┬──────────────────┬───────────────┘  │
│           │                  │                   │
│           ▼                  ▼                   │
│  ┌─────────────────┐  ┌──────────────────┐     │
│  │ LLM Integration │  │ Supabase Client  │     │
│  │    (llm.py)     │  │   (SDK 2.10.0)   │     │
│  └────────┬────────┘  └────────┬─────────┘     │
└───────────┼─────────────────────┼───────────────┘
            │                     │
            ▼                     ▼
┌────────────────────┐  ┌─────────────────────┐
│  GitHub Models     │  │  Supabase Cloud     │
│  (OpenAI API)      │  │  (PostgreSQL DB)    │
└────────────────────┘  └─────────────────────┘
```

### Local Development

1. **Clone and install dependencies:**
   ```bash
   git clone https://github.com/yausum/Notetaking-App.git
   cd Notetaking-App
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (see Installation section)

3. **Run development server:**
   ```bash
   python run.py
   ```
   
   Runs on `http://localhost:5000` with debug mode enabled:
   - Auto-reload on code changes
   - Detailed error pages
   - Interactive debugger

### Folder Structure Details

- **Backend Logic**: `backend/app.py` (500+ lines)
- **AI Integration**: `backend/llm.py` (~200 lines)
- **Frontend Templates**: `frontend/templates/*.html` (7 templates)
- **Styling**: `frontend/static/style.css` (1000+ lines)
- **Interactivity**: `frontend/static/script.js` (~300 lines)
- **Database Init**: `init_supabase.py`
- **Entry Point**: `run.py` (Vercel-compatible)

### Dependencies

See `requirements.txt` for full list. Key packages:

```
Flask==3.0.0              # Web framework
Werkzeug==3.0.1           # WSGI utilities
supabase==2.10.0          # Supabase Python client
openai==1.106.1           # OpenAI API client
python-dotenv==1.0.0      # Environment variable management
```

### Debug Mode

The app runs with these configurations:

```python
# run.py
if __name__ == '__main__':
    try:
        init_db()  # Only for local development
    except:
        pass  # Skip in serverless environment
    app.run(debug=True, host='0.0.0.0', port=5000)
```

This enables:
- Auto-reload on code changes
- Detailed error pages
- Interactive debugger
- CORS headers for API testing

## 🚢 Deployment

### Vercel (Recommended)

This app is optimized for Vercel serverless deployment:

1. **Prepare your repository:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Vercel:**
   - Visit [vercel.com](https://vercel.com) and sign in
   - Click "Import Project"
   - Connect your GitHub repository
   - Vercel auto-detects the Flask configuration

3. **Configure environment variables:**
   - In Vercel dashboard → Project Settings → Environment Variables
   - Add all variables from your `.env` file:
     - `GITHUB_TOKEN`
     - `OPENAI_MODEL`
     - `SUPABASE_URL`
     - `SUPABASE_KEY`

4. **Deploy and access:**
   - Vercel provides a production URL
   - Automatic deployments on git push
   - Preview deployments for pull requests

### Other Platforms

The app can also be deployed to:
- **Heroku**: Add `Procfile` with `web: python run.py`
- **Railway**: Auto-detects Flask apps
- **Render**: Use Python runtime
- **PythonAnywhere**: Traditional hosting with WSGI

### Known Issues & Solutions

**CSS Not Loading on Vercel:**
- ✅ Fixed by adding explicit static file route handler in `app.py`
- Uses `send_from_directory()` for static files

**Environment Variables:**
- Ensure all variables are set in deployment platform
- Never commit `.env` to git

**Database Connection:**
- Use Supabase connection pooler for better performance
- Enable SSL mode for secure connections

## � Project Statistics

- **Total Lines of Code**: ~2,500+
- **Backend Code**: ~700 lines (Python)
- **Frontend Code**: ~1,300 lines (HTML/CSS/JS)
- **Templates**: 7 Jinja2 files
- **API Endpoints**: 8 routes (4 AI-powered)
- **Database Tables**: 1 (with 3 indexes)
- **Supported Languages**: 10 (for translation/generation)
- **Deployment Platform**: Vercel (Serverless)

## 🐛 Troubleshooting

### Common Issues

1. **"Error loading notes" when sorting by event date:**
   - **Cause**: Incorrect parameter name in Supabase SDK
   - **Solution**: Use `nullsfirst=False` instead of `nulls_first=False`
   - **Fixed in**: Latest commit (Oct 25, 2025)

2. **CSS not loading on Vercel:**
   - **Cause**: Serverless functions don't auto-serve static files
   - **Solution**: Added explicit `/static/<path>` route with `send_from_directory()`

3. **AI features not working:**
   - Check `GITHUB_TOKEN` is valid and has proper permissions
   - Verify `OPENAI_MODEL` is set correctly (e.g., `gpt-4o-mini`)
   - Check rate limits on GitHub Models API

4. **Database connection errors:**
   - Ensure Supabase credentials are correct in `.env`
   - Verify the `notes` table exists (run `init_supabase.py`)
   - Check Supabase project is not paused (free tier auto-pauses)


## �📄 License

This project is for educational purposes (COMP5421 Lab2).

## 👨‍💻 Author

**yausum**
- GitHub: [@yausum](https://github.com/yausum)

## 🙏 Acknowledgments

- Flask documentation and community
- Supabase for excellent database platform
- OpenAI/GitHub for AI model access
- Vercel for serverless deployment
- COMP5421 course staff

---

**Built with Flask, Supabase PostgreSQL, OpenAI, and ❤️**

**Last Updated**: October 25, 2025
