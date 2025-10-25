# Lab 2 Writeup - Note-Taking Application with AI Features

**Course**: COMP5421 - Software Engineering And Development
**Student**: 24120919g Yau Ming Sum  
**Repository**: [yausum/Notetaking-App](https://github.com/yausum/Notetaking-App)  
**Deployed URL**: [https://notetaking-app.vercel.app](https://notetaking-9v26e1vkq-yau-ming-sums-projects.vercel.app/)


## 🎯 Project Overview

This project is a **full-stack note-taking web application** featuring AI-powered capabilities for note generation, translation, and smart categorization. The application allows users to create, edit, search, and organize notes with optional event dates and times.

### Key Features

- ✅ **CRUD Operations**: Create, Read, Update, Delete notes
- ✅ **AI-Powered Generation**: Convert natural language to structured notes
- ✅ **Multi-language Translation**: Translate notes to 10 different languages
- ✅ **Smart Tagging**: Auto-generate relevant tags (max 3 per note)
- ✅ **Event Tracking**: Optional date/time fields for events and deadlines
- ✅ **Search & Sort**: Full-text search with multiple sorting options
- ✅ **Responsive Design**: Mobile-friendly interface with purple gradient theme
- ✅ **Cloud Database**: Supabase PostgreSQL for scalable data storage
- ✅ **Serverless Deployment**: Vercel for global edge deployment

---

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Supabase** - PostgreSQL database with Python SDK
- **OpenAI API** - Via GitHub Models endpoint for AI features
- **python-dotenv** - Environment variable management

### Frontend
- **Jinja2** - Server-side templating
- **Vanilla JavaScript (ES6+)** - Client-side interactivity with async/await
- **CSS3** - Responsive design with Flexbox/Grid
- **HTML5** - Semantic markup

### Deployment & DevOps
- **Vercel** - Serverless hosting platform
- **GitHub** - Version control and CI/CD
- **GitHub Copilot** - AI-assisted development

### AI Integration
- **GitHub Models API** - Access to OpenAI GPT-4.1-mini
- **Temperature Control**: 0.3 for structured extraction, 0.7 for creative generation

---

## 🚀 Development Process and steps

### Phase 1: Initial Setup (SQLite Version)

**Steps:**
1. Created Flask application structure with MVC pattern
2. Implemented SQLite database with `notes` table
3. Built CRUD operations with server-side rendering
4. Designed responsive UI with purple gradient theme
5. Added search functionality with sorting options

**Code Structure:**
```
Notetaking-App/
├── backend/
│   ├── app.py              # Flask routes and logic
│   └── llm.py              # AI integration
├── frontend/
│   ├── static/
│   │   ├── style.css       # Styling
│   │   └── script.js       # Client-side JS
│   └── templates/          # Jinja2 templates
├── database/
│   └── notes.db            # SQLite database
└── run.py                  # Entry point
```

### Phase 2: AI Features Integration

**Implemented Features:**

1. **AI Note Generation** (`/api/generate-note`)
   - Natural language input → Structured JSON output
   - Extracts: Title, Content, Category, Tags, Event Date/Time
   - Date parsing (e.g., "tomorrow 5pm" → "2025-10-26", "17:00")
   - Preview before save functionality

2. **Translation** (`/api/translate`)
   - 10 supported languages
   - Real-time translation of title and content
   - Maintains original note structure

3. **Auto-Tagging** (`/api/generate-tags`)
   - Generates up to 3 relevant keywords
   - Based on title and content analysis

4. **Summarization** (`/api/summarize`)
   - Creates concise summaries
   - Configurable max length

**AI System Prompt Example:**
```python
system_prompt = f"""Extract the user's notes into structured fields:
1. Title: A concise title less than 5 words
2. Notes: Full sentences based on user input
3. Category: Single category (Work, Personal, Study, etc.)
4. Tags: At most 3 keywords
5. EventDate: YYYY-MM-DD format (null if not available)
6. EventTime: HH:MM 24-hour format (null if not available)

Output in JSON format. Language: {language}.

Date parsing rules:
- "tomorrow" = next day
- "next Monday" = next occurrence
- "5pm" = "17:00"

Example:
Input: "Badminton tmr 5pm @polyu"
Output: {{"Title": "Badminton at PolyU", ...}}
"""
```

### Phase 3: Database Migration (SQLite → Supabase)

**Why Migrate?**
- ✅ Cloud-hosted (no local file dependency)
- ✅ Better scalability for multiple users
- ✅ Automatic backups
- ✅ Real-time capabilities
- ✅ ACID compliance with PostgreSQL

**Migration Steps:**

#### Step 1: Setup Supabase Project
1. Created account at [supabase.com](https://supabase.com)
2. Created new project with PostgreSQL database
3. Obtained connection credentials:
   - Project URL: `https://[project-ref].supabase.co`
   - Anon Key: Public API key for client SDK

#### Step 2: Updated Dependencies
```diff
# requirements.txt
Flask==3.0.0
Werkzeug==3.0.1
python-dotenv==1.0.0
openai==1.106.1
- sqlite3 (built-in)
+ supabase==2.10.0
```

#### Step 3: Modified Database Connection
```python
# OLD (SQLite)
import sqlite3
conn = sqlite3.connect('database/notes.db')
cursor = conn.execute('SELECT * FROM notes WHERE id = ?', (id,))

# NEW (Supabase)
from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
response = supabase.table('notes').select('*').eq('id', id).execute()
```

#### Step 4: Created Database Schema
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

-- Indexes for performance
CREATE INDEX idx_notes_updated_at ON notes(updated_at DESC);
CREATE INDEX idx_notes_event_date ON notes(event_date DESC);
CREATE INDEX idx_notes_created_at ON notes(created_at DESC);

-- Row Level Security
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all operations for notes" 
ON notes FOR ALL USING (true) WITH CHECK (true);
```

#### Step 5: Updated All Database Queries

**Example: Add Note**
```python
# OLD
cursor = conn.execute(
    'INSERT INTO notes (title, content) VALUES (?, ?)',
    (title, content)
)
note_id = cursor.lastrowid

# NEW
response = supabase.table('notes').insert({
    'title': title,
    'content': content
}).execute()
note_id = response.data[0]['id']
```

**Example: Search**
```python
# OLD
notes = conn.execute(
    'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?',
    (f'%{query}%', f'%{query}%')
).fetchall()

# NEW
response = supabase.table('notes').select('*').or_(
    f"title.ilike.%{query}%,content.ilike.%{query}%"
).execute()
notes = response.data
```

### Phase 4: Deployment to Vercel

**Why Vercel?**
- ✅ Free tier suitable for personal projects
- ✅ Automatic deployments from GitHub
- ✅ Global edge network (fast worldwide)
- ✅ Built-in CI/CD
- ✅ Environment variable management

**Deployment Steps:**

#### Step 1: Created `vercel.json`
```json
{
  "version": 2,
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

#### Step 2: Fixed Static Files Issue

**Challenge**: CSS and JS files not loading after deployment

**Solution**: Added explicit static file route
```python
from flask import send_from_directory

@app.route('/static/<path:filename>')
def serve_static(filename):
    static_dir = os.path.join(BASE_DIR, 'frontend', 'static')
    return send_from_directory(static_dir, filename)
```

#### Step 3: Configured Environment Variables

In Vercel Dashboard → Settings → Environment Variables:
- `GITHUB_TOKEN` - For OpenAI API access via GitHub Models
- `OPENAI_MODEL` - Model identifier (openai/gpt-4.1-mini)
- `SUPABASE_URL` - Database project URL
- `SUPABASE_KEY` - Database anon public key

#### Step 4: Updated `run.py` for Serverless

```python
# Initialize database (skip in serverless)
try:
    init_db()
except Exception as e:
    print(f"Note: Database initialization skipped - {e}")

# Export app for Vercel
app = app  # Vercel uses this 'app' object
```

#### Step 5: GitHub Integration

1. Pushed code to GitHub repository
2. Imported project in Vercel from GitHub
3. Configured build settings (automatic)
4. Deployed! 🚀

**Automatic Redeployment:**
```bash
git add .
git commit -m "Update feature"
git push origin main
# Vercel automatically redeploys!
```

---

## 💡 Challenges and Solutions

### Challenge 1: Database Migration Complexity

**Problem**: Converting all SQLite queries to Supabase SDK syntax
- SQLite uses `?` placeholders, Supabase uses method chaining
- `cursor.lastrowid` vs `RETURNING id`
- Different error handling patterns

**Solution**:
1. Created migration guide documenting all syntax changes
2. Updated queries incrementally, testing each route
3. Used try-except blocks for robust error handling
4. Tested locally before deploying

**Code Comparison:**
```python
# SQLite - Parameterized query
conn.execute('UPDATE notes SET title=? WHERE id=?', (title, id))

# Supabase - Method chaining
supabase.table('notes').update({'title': title}).eq('id', id).execute()
```

### Challenge 2: CSS Not Loading on Vercel

**Problem**: After deployment, CSS and JavaScript files returned 404 errors

**Root Cause**: Vercel's serverless functions don't automatically serve Flask static files

**Solution**:
1. Added explicit route handler for static files
2. Used `send_from_directory()` to serve CSS/JS
3. Configured `static_url_path='/static'` in Flask app
4. Simplified `vercel.json` to route all requests to Flask

**Before:**
```json
"routes": [
  {"src": "/static/(.*)", "dest": "/frontend/static/$1"},
  {"src": "/(.*)", "dest": "run.py"}
]
```

**After:**
```json
"routes": [
  {"src": "/(.*)", "dest": "run.py"}
]
```

With explicit Python handler:
```python
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_dir, filename)
```

### Challenge 3: Environment Variables Security

**Problem**: Need to use API keys without committing them to GitHub

**Solution**:
1. Created `.env` file for local development
2. Added `.env` to `.gitignore`
3. Set environment variables in Vercel Dashboard
4. Used `python-dotenv` to load variables
5. Documented required variables in README

```python
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
```

### Challenge 4: AI Response Parsing

**Problem**: LLM sometimes returns extra text besides JSON, causing parsing errors

**Solution**:
1. Extract JSON substring using string operations
2. Implement fallback to raw text if JSON parsing fails
3. Validate extracted fields with default values

```python
try:
    # Find JSON in response
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}') + 1
    json_str = response_text[start_idx:end_idx]
    note_data = json.loads(json_str)
except:
    # Fallback to raw text
    note_data = {
        'title': 'Generated Note',
        'content': response_text,
        'category': '',
        'tags': ''
    }
```

### Challenge 5: Date/Time Natural Language Parsing

**Problem**: Users input dates in various formats ("tomorrow", "next Friday", "5pm")

**Solution**:
1. Defined clear parsing rules in system prompt
2. Provided examples for common patterns
3. Used specific output format (YYYY-MM-DD, HH:MM)
4. Handled null values for missing dates

**Parsing Rules in Prompt:**
```
Date parsing rules:
- "tomorrow" = next day
- "next Monday" = next occurrence of that weekday
- "Jan 15" = current year if not specified
- "5pm" = "17:00"
- "noon" = "12:00"
```

---

## 📚 Lessons Learned

### 1. Cloud Databases vs Local Databases

**SQLite Pros:**
- ✅ Simple setup (single file)
- ✅ No network dependency
- ✅ Good for development

**SQLite Cons:**
- ❌ Single-user (file locking issues)
- ❌ Limited scalability
- ❌ Manual backups

**Supabase PostgreSQL Pros:**
- ✅ Cloud-hosted (accessible anywhere)
- ✅ Multi-user support
- ✅ Automatic backups
- ✅ Scalable
- ✅ Real-time capabilities

**Supabase Cons:**
- ❌ Requires internet connection
- ❌ More complex setup initially
- ❌ Free tier limitations (500MB, 2GB bandwidth)

**Takeaway**: For production web apps, cloud databases are essential for scalability and reliability.

### 2. Serverless Deployment Considerations

**Key Learnings:**
- Serverless functions are stateless (no persistent storage)
- Database tables must be pre-created (can't create on-the-fly)
- Static file serving requires explicit configuration
- Environment variables must be set in platform (not `.env`)
- Cold starts can cause first request to be slower

**Best Practice**: Separate database initialization from application code

### 3. AI Prompt Engineering

**Effective Strategies:**
1. **Be Specific**: Define exact output format (JSON structure)
2. **Provide Examples**: Show expected input/output pairs
3. **Set Constraints**: Limit tags to 3, titles to 5 words
4. **Handle Edge Cases**: Define behavior for missing data
5. **Use Right Temperature**: 0.3 for extraction, 0.7 for creativity

**Example of Good Prompt:**
```python
system_prompt = f"""
Extract structured fields from user input.
Output JSON format WITHOUT ```json wrapper.
Language: {language}

Fields:
1. Title: Max 5 words
2. Notes: Full sentences
3. Category: One of [Work, Personal, Study, Health, Finance]
4. Tags: Array of max 3 keywords
5. EventDate: YYYY-MM-DD or null
6. EventTime: HH:MM or null

Example:
Input: "Team meeting tomorrow 2pm discuss Q4 goals"
Output: {{"Title": "Q4 Goals Meeting", "Notes": "...}}
"""
```

### 4. Version Control with GitHub

**Good Practices:**
- ✅ Frequent commits with clear messages
- ✅ Use `.gitignore` for secrets and dependencies
- ✅ Create feature branches for major changes
- ✅ Document changes in commit messages
- ✅ Use GitHub Issues to track tasks

**Commit Message Examples:**
```bash
git commit -m "Add AI note generation feature"
git commit -m "Fix: CSS not loading on Vercel deployment"
git commit -m "Migrate database from SQLite to Supabase"
```

### 5. Error Handling and User Experience

**Key Principles:**
- Always show loading indicators during async operations
- Provide clear error messages (user-friendly, not technical)
- Use try-catch-finally for cleanup (hide loading indicators)
- Flash messages for feedback (success, error, warning)
- Graceful degradation (fallback when AI fails)

```javascript
try {
    showLoading();
    const result = await apiCall();
    showSuccess('Note created!');
} catch (error) {
    showError('Failed to create note. Please try again.');
} finally {
    hideLoading();
}
```

### 6. GitHub Copilot as Development Assistant

**How I Used Copilot:**
- 🤖 Code completion for repetitive patterns
- 🤖 Generating boilerplate code (routes, forms)
- 🤖 Suggesting error handling patterns
- 🤖 Creating documentation and comments
- 🤖 Debugging assistance

**Copilot Instructions:**
Created `.github/copilot-instructions.md` to define:
- Project-specific coding standards
- Naming conventions
- Database access patterns
- Error handling strategies
- AI integration guidelines

**Result**: More consistent code, faster development, fewer bugs

---

## 🚀 Future Improvements

### 1. User Authentication
- Add Supabase Auth for user accounts
- Make notes private per user (Row Level Security)
- Implement user profiles and preferences

### 2. File Attachments
- Use Supabase Storage for images/documents
- Allow attaching files to notes
- Preview images inline

### 3. Real-time Collaboration
- Use Supabase Real-time subscriptions
- Live updates across multiple devices
- Collaborative editing

### 4. Advanced AI Features
- Voice-to-note transcription
- Image-to-note (OCR)
- Smart reminders based on event dates
- Category auto-assignment

### 5. Mobile App
- React Native mobile app
- Offline mode with sync
- Push notifications for reminders

### 6. Export/Import
- Export notes to PDF, Markdown, or JSON
- Import from Evernote, Google Keep
- Bulk operations

### 7. Performance Optimization
- Implement pagination for large note lists
- Cache frequently accessed data
- Lazy loading for images

---

## 📸 Screenshots

### 1. Home Page - Notes List
![Home Page](screenshots/home-page.png)
*Caption: Main dashboard showing all notes with sorting options and search bar*

### 2. AI Note Generation
![AI Generation](screenshots/ai-generate.png)
*Caption: Natural language input converted to structured note with preview*

### 3. Note Detail View
![Note View](screenshots/note-detail.png)
*Caption: Single note view with edit and delete options*

### 4. Edit Note Form
![Edit Form](screenshots/edit-note.png)
*Caption: Form with all fields including AI-generated category and tags*

### 5. Search Results
![Search](screenshots/search-results.png)
*Caption: Full-text search across title, content, category, and tags*

### 6. Translation Feature
![Translation](screenshots/translation.png)
*Caption: Translating note to 中文(繁體)*

### 7. Mobile Responsive View
![Mobile](screenshots/mobile-view.png)
*Caption: Mobile-optimized interface with hamburger menu*

### 8. Supabase Database
![Database](screenshots/supabase-db.png)
*Caption: Notes table in Supabase Table Editor*

### 9. Vercel Deployment
![Vercel](screenshots/vercel-deployment.png)
*Caption: Successful deployment on Vercel with automatic CI/CD*

---

## 📊 Project Statistics

- **Total Lines of Code**: ~2,500
  - Python (Backend): ~800 lines
  - JavaScript (Frontend): ~300 lines
  - CSS: ~1,200 lines
  - HTML (Templates): ~200 lines

- **Development Time**: ~20 hours
  - Initial setup: 4 hours
  - AI features: 6 hours
  - Database migration: 4 hours
  - Deployment & debugging: 4 hours
  - Documentation: 2 hours

- **GitHub Commits**: 50+
- **Features Implemented**: 12+
- **API Endpoints**: 8

---

## 🔗 Links and Resources

- **GitHub Repository**: https://github.com/yausum/Notetaking-App
- **Live Demo**: https://notetaking-app.vercel.app
- **Supabase**: https://supabase.com
- **Vercel**: https://vercel.com
- **Flask Documentation**: https://flask.palletsprojects.com/
- **OpenAI API**: https://platform.openai.com/docs

---

## 📝 Conclusion

This project successfully demonstrates a modern full-stack web application with AI integration, cloud database, and serverless deployment. The migration from SQLite to Supabase PostgreSQL showcased the benefits of cloud-hosted databases for scalability and reliability. Deployment on Vercel with automatic CI/CD streamlined the development workflow.

Key achievements:
- ✅ Functional CRUD application with AI-powered features
- ✅ Successful database migration with zero data loss
- ✅ Production deployment with global availability
- ✅ Responsive design working across devices
- ✅ Secure environment variable management
- ✅ Well-documented codebase with GitHub Copilot instructions

The challenges faced during development—particularly with static file serving and AI response parsing—provided valuable learning experiences in serverless architecture and prompt engineering. These lessons will be invaluable for future cloud-based projects.

---

**End of Lab 2 Writeup**  
**Date Completed**: October 25, 2025  
**Student**: Sam

## Challange
![alt text](image.png)
![alt text](image-1.png)
When in development, sometimes it has bugs and i will provide a screenshot to the AI as a reference to solve the issue.


![alt text](image-2.png)
provide layout for AI as a reference when in development process
