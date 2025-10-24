# 📝 GitHub Copilot Instructions - Notetaking App

## 🎯 Project Overview

This is a **full-stack note-taking web application** built with Flask, SQLite, and vanilla JavaScript. It features AI-powered note generation, translation, and smart categorization using OpenAI/GitHub Models API.

**Tech Stack:**
- **Backend**: Flask 3.0.0, SQLite3, Python 3.x
- **Frontend**: Jinja2 templates, vanilla JavaScript (ES6+), CSS3
- **AI Integration**: OpenAI API via GitHub Models endpoint
- **Architecture**: Traditional server-side rendering with AJAX for AI features

---

## 📂 Project Structure

```
Notetaking-App/
├── backend/
│   ├── app.py              # Flask routes, database logic, API endpoints
│   └── llm.py              # LLM integration (OpenAI/GitHub Models)
├── frontend/
│   ├── static/
│   │   ├── style.css       # Single CSS file (1000+ lines)
│   │   └── script.js       # Global JS utilities
│   └── templates/          # Jinja2 templates
│       ├── base.html       # Master layout with navigation
│       ├── index.html      # Home page (all notes)
│       ├── add_note.html   # Create note form
│       ├── edit_note.html  # Edit note form
│       ├── view_note.html  # View single note
│       ├── search.html     # Search results
│       └── generate_note.html  # AI note generation
├── database/
│   └── notes.db            # SQLite database (auto-generated)
├── .env                    # Environment variables (GITHUB_TOKEN, etc.)
└── run.py                  # Application entry point
```

---

## 🗄️ Database Schema

**Table: `notes`**
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,              -- AI-generated or user-defined
    tags TEXT,                  -- Comma-separated, max 3
    event_date DATE,            -- YYYY-MM-DD format
    event_time TIME,            -- HH:MM 24-hour format
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## 🎨 Coding Standards

### Python (Backend)

1. **Function Naming**: Use `snake_case` for all functions and variables
   ```python
   def get_db_connection():
   def init_db():
   def api_generate_note():
   ```

2. **Route Naming**: 
   - Page routes: `/`, `/add`, `/edit/<id>`, `/note/<id>`
   - API routes: `/api/translate`, `/api/generate-note`, `/api/generate-tags`

3. **Database Connections**:
   - Always use `get_db_connection()` function
   - Use context managers or explicit `.close()`
   - Set `conn.row_factory = sqlite3.Row` for dict-like access

4. **Error Handling**:
   ```python
   try:
       # Database or LLM operations
   except Exception as e:
       return jsonify({'success': False, 'error': str(e)}), 500
   ```

5. **JSON Responses**:
   ```python
   return jsonify({
       'success': True,
       'data': result
   })
   ```

6. **LLM Integration**:
   - Import from `backend.llm`: `call_llm_model`, `translate_text`, `generate_tags`
   - Always use temperature `0.3` for structured extraction
   - Always use temperature `0.7` for creative generation

### JavaScript (Frontend)

1. **Function Naming**: Use `camelCase`
   ```javascript
   async function generateNote() {}
   function showPreview(note) {}
   ```

2. **Async/Await**: Always use async/await for API calls (no `.then()` chains)
   ```javascript
   const response = await fetch('/api/endpoint', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(data)
   });
   const result = await response.json();
   ```

3. **Error Handling**:
   ```javascript
   try {
       // API calls
   } catch (error) {
       alert('Error: ' + error.message);
   } finally {
       // Hide loading indicators
   }
   ```

4. **DOM Manipulation**: Use vanilla JavaScript (no jQuery)
   ```javascript
   document.getElementById('elementId')
   element.style.display = 'flex'
   ```

### CSS

1. **Class Naming**: Use `kebab-case` with semantic names
   ```css
   .form-group
   .btn-primary
   .preview-section
   ```

2. **Color Scheme**: Purple gradient theme
   - Primary: `#667eea` to `#764ba2`
   - Accent: `#f093fb` to `#f5576c`
   - Background: `#f8f9fc`

3. **Layout**: Flexbox-first approach, CSS Grid for complex layouts

4. **Responsive**: Mobile-first with breakpoints at 768px

---

## 🤖 AI Feature Guidelines

### System Prompt Structure

When creating AI features, follow this structured extraction pattern:

```python
system_prompt = f"""Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Category: A single category (Work, Personal, Study, Health, Finance, Travel, Shopping, Ideas)
4. Tags (A list): At most 3 Keywords or tags
5. EventDate (optional): YYYY-MM-DD format. Use null if not available.
6. EventTime (optional): HH:MM 24-hour format. Use null if not available.
Output in JSON format without ```json. Output in language: {language}.

[Include parsing rules for dates/times]
[Include examples with expected output]
"""
```

### AI Response Processing

1. **Always extract JSON from LLM response**:
   ```python
   start_idx = response_text.find('{')
   end_idx = response_text.rfind('}') + 1
   json_str = response_text[start_idx:end_idx]
   note_data = json.loads(json_str)
   ```

2. **Handle fallback cases**:
   - JSON parsing fails → Use raw text
   - Missing fields → Provide sensible defaults

3. **Null handling for optional fields**:
   ```python
   if event_date == 'null' or event_date == '':
       event_date = None
   ```

### Date/Time Parsing Rules

Include these in system prompts:
```
Date parsing rules:
- "tomorrow" = next day
- "next Monday/Tuesday/etc" = next occurrence
- "Jan 15", "15 Jan", "January 15" = current year

Time parsing rules:
- "5pm" = "17:00"
- "9am" = "09:00"
- "noon" = "12:00"
- "midnight" = "00:00"
```

---

## 🔄 Workflow Patterns

### AJAX Form Submission

When a form needs to return data (not just redirect):

**Backend:**
```python
@app.route('/add', methods=['POST'])
def add_note():
    # Process form data
    cursor = conn.execute('INSERT INTO notes (...) VALUES (...)', (...))
    note_id = cursor.lastrowid
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'note_id': note_id})
    
    # Regular form submission
    flash('Note created!', 'success')
    return redirect(url_for('index'))
```

**Frontend:**
```javascript
const formData = new FormData();
formData.append('title', title);
// ... other fields

const response = await fetch('/add', {
    method: 'POST',
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
    body: formData
});

const data = await response.json();
if (data.success) {
    window.location.href = '/';  // Redirect to home
}
```

### Loading Indicators

Always show/hide loading states:

```javascript
// Show loading
document.getElementById('loadingIndicator').style.display = 'flex';

try {
    // Async operation
} finally {
    // Hide loading
    document.getElementById('loadingIndicator').style.display = 'none';
}
```

### Preview Before Save

For AI-generated content:
1. Generate → Show preview (editable fields)
2. User reviews → Can modify
3. Save → Redirect to home page

---

## 🌍 Translation Feature

### Supported Languages

10 languages in dropdown:
- English, 中文 (繁體), 中文 (简体), 日本語, 한국어
- Español, Français, Deutsch, Italiano, Português

### Implementation Pattern

```javascript
async function translateText(sourceText, targetLang) {
    const response = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: sourceText,
            target_language: targetLang
        })
    });
    const data = await response.json();
    return data.translated_text;
}
```

---

## 📝 Note Form Standards

### Required Fields
- **Title**: Text input, required, placeholder "Enter note title"
- **Content**: Textarea, required, rows="10"

### Optional Fields
- **Category**: Text input, can be auto-generated by AI
- **Tags**: Text input, comma-separated, max 3
- **Event Date**: `<input type="date">` (HTML5)
- **Event Time**: `<input type="time">` (HTML5)

### Form Layout
```html
<form method="POST" action="/add">
    <div class="form-group">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" required>
    </div>
    <!-- More fields -->
    <div class="form-actions">
        <button type="submit" class="btn-primary">Save</button>
        <a href="/" class="btn-secondary">Cancel</a>
    </div>
</form>
```

---

## 🎯 Business Logic Rules

### Category Assignment
- AI should suggest one of: Work, Personal, Study, Health, Finance, Travel, Shopping, Ideas
- User can override in edit mode

### Tags Generation
- Maximum 3 tags per note
- Comma-separated in database
- AI should generate relevant, concise keywords

### Date/Time Handling
- Both are optional (can be NULL)
- Use for events, deadlines, appointments
- Display in preview if extracted by AI
- User can modify before saving

### Sorting Options
- **Default**: `updated_at DESC` (most recently updated first)
- **Event Date**: `event_date ASC` (NULL values last)
- Dropdown on home page

---

## 🚨 Common Patterns to Follow

### When Adding New AI Features:

1. **Create API endpoint** in `app.py`:
   ```python
   @app.route('/api/new-feature', methods=['POST'])
   def api_new_feature():
       data = request.get_json()
       # Call LLM helper from backend.llm
       # Return JSON response
   ```

2. **Add helper function** in `llm.py`:
   ```python
   def new_feature(input_text, **kwargs):
       messages = [{"role": "system", "content": system_prompt},
                   {"role": "user", "content": input_text}]
       return call_llm_model(messages, temperature=0.3)
   ```

3. **Add frontend button** and async handler:
   ```javascript
   async function handleNewFeature() {
       const response = await fetch('/api/new-feature', {...});
       const data = await response.json();
       // Update UI
   }
   ```

### When Modifying Templates:

1. **Always extend** `base.html`
2. **Use blocks**: `{% block title %}`, `{% block content %}`, `{% block scripts %}`
3. **Include CSRF** if needed (currently not implemented)
4. **Flash messages** for user feedback

### Error Messages:

- **User-facing**: Simple, actionable (e.g., "Failed to generate note. Please try again.")
- **Logging**: Include full error details
- **API responses**: Include error field with description

---

## 🔒 Security Notes

1. **API Keys**: Store in `.env`, never commit
2. **Input Validation**: Validate on backend, not just frontend
3. **SQL Injection**: Use parameterized queries (always use `?` placeholders)
4. **XSS Prevention**: Jinja2 auto-escapes, but be careful with `|safe` filter

---

## 🧪 Testing Guidelines

### Manual Testing Checklist for AI Features:

- [ ] Test with various natural language inputs
- [ ] Test with different languages
- [ ] Test with and without date/time mentions
- [ ] Test fallback when JSON parsing fails
- [ ] Verify NULL handling in database
- [ ] Check loading indicators show/hide correctly
- [ ] Verify redirect after save

### Date Extraction Test Cases:

- "tomorrow 5pm" → Extract next day + 17:00
- "next Monday 3pm" → Extract next Monday + 15:00
- "Jan 15 9am" → Extract date + 09:00
- "no date mentioned" → NULL for both

---

## 📚 Reference Files

- **API Documentation**: `API_DOCUMENTATION.md`
- **System Prompt Spec**: `SYSTEM_PROMPT_SPEC.md`
- **Enhanced Features**: `ENHANCED_FEATURES.md`
- **Translation Guide**: `TRANSLATION_GUIDE.md`
- **Generate Feature**: `GENERATE_NOTE_GUIDE.md`

---

## 🎓 Key Principles

1. **Consistency**: Follow existing patterns in the codebase
2. **Simplicity**: Use vanilla JS/CSS, avoid unnecessary frameworks
3. **User Experience**: Always provide feedback (loading, success, errors)
4. **AI Integration**: Structured prompts with examples and fallbacks
5. **Maintainability**: Clear function names, comments for complex logic
6. **Performance**: Minimize database queries, use efficient SQL

---

## 💡 When in Doubt:

1. Check existing similar features in the codebase
2. Follow the patterns in `app.py` for routes
3. Follow the patterns in `llm.py` for AI features
4. Use `generate_note.html` as reference for AI features with preview
5. Match the existing purple gradient design theme

---

**Last Updated**: October 24, 2025  
**Project**: COMP5421 Lab2 - Note Taking App  
**Author**: GitHub Copilot Instructions
