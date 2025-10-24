from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os
from backend.llm import translate_text, generate_tags, summarize_note

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure Flask to use frontend folder for templates and static files
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'frontend', 'static'))
app.secret_key = 'your-secret-key-here'

# Database path in database folder
DATABASE = os.path.join(BASE_DIR, 'database', 'notes.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            event_date DATE,
            event_time TIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'updated')
    
    conn = get_db_connection()
    
    # Determine sort order
    if sort_by == 'event_date':
        # Sort by event date, putting NULL values last
        notes = conn.execute('SELECT * FROM notes ORDER BY CASE WHEN event_date IS NULL THEN 1 ELSE 0 END, event_date DESC, event_time DESC').fetchall()
    elif sort_by == 'event_time':
        # Sort by event time, putting NULL values last
        notes = conn.execute('SELECT * FROM notes ORDER BY CASE WHEN event_time IS NULL THEN 1 ELSE 0 END, event_time DESC, event_date DESC').fetchall()
    elif sort_by == 'created':
        notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
    elif sort_by == 'title':
        notes = conn.execute('SELECT * FROM notes ORDER BY title ASC').fetchall()
    else:  # default: updated
        notes = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC').fetchall()
    
    conn.close()
    return render_template('index.html', notes=notes, sort_by=sort_by)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        tags = request.form.get('tags', '')
        event_date = request.form.get('event_date', '')
        event_time = request.form.get('event_time', '')
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('add_note'))
        
        conn = get_db_connection()
        cursor = conn.execute('INSERT INTO notes (title, content, category, tags, event_date, event_time) VALUES (?, ?, ?, ?, ?, ?)',
                     (title, content, category, tags, event_date, event_time))
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Check if this is from generate page (AJAX request)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'note_id': note_id})
        
        flash('Note added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_note.html')

@app.route('/generate')
def generate_note():
    return render_template('generate_note.html')

@app.route('/note/<int:id>')
def view_note(id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if note is None:
        flash('Note not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('view_note.html', note=note)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (id,)).fetchone()
    
    if note is None:
        conn.close()
        flash('Note not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        tags = request.form.get('tags', '')
        event_date = request.form.get('event_date', '')
        event_time = request.form.get('event_time', '')
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('edit_note', id=id))
        
        conn.execute('UPDATE notes SET title = ?, content = ?, category = ?, tags = ?, event_date = ?, event_time = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                     (title, content, category, tags, event_date, event_time, id))
        conn.commit()
        conn.close()
        
        flash('Note updated successfully!', 'success')
        return redirect(url_for('view_note', id=id))
    
    conn.close()
    return render_template('edit_note.html', note=note)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'updated')
    
    if query:
        conn = get_db_connection()
        
        # Build the base search query
        base_query = 'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR category LIKE ? OR tags LIKE ?'
        params = (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%')
        
        # Add sorting
        if sort_by == 'event_date':
            order_clause = ' ORDER BY CASE WHEN event_date IS NULL THEN 1 ELSE 0 END, event_date DESC, event_time DESC'
        elif sort_by == 'event_time':
            order_clause = ' ORDER BY CASE WHEN event_time IS NULL THEN 1 ELSE 0 END, event_time DESC, event_date DESC'
        elif sort_by == 'created':
            order_clause = ' ORDER BY created_at DESC'
        elif sort_by == 'title':
            order_clause = ' ORDER BY title ASC'
        else:  # default: updated
            order_clause = ' ORDER BY updated_at DESC'
        
        notes = conn.execute(base_query + order_clause, params).fetchall()
        conn.close()
    else:
        notes = []
    
    return render_template('search.html', notes=notes, query=query, sort_by=sort_by)

@app.route('/api/notes')
def api_notes():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(note) for note in notes])

# ============================================
# LLM API Routes
# ============================================

@app.route('/api/translate', methods=['POST'])
def api_translate():
    """
    Translate text to target language
    POST body: {"text": "content", "target_language": "Chinese"}
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_language = data.get('target_language', 'Chinese')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        translated_text = translate_text(text, target_language)
        
        return jsonify({
            'success': True,
            'original': text,
            'translated': translated_text,
            'target_language': target_language
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-tags', methods=['POST'])
def api_generate_tags():
    """
    Generate tags from title and content
    POST body: {"title": "...", "content": "...", "max_tags": 5}
    """
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')
        max_tags = data.get('max_tags', 5)
        
        if not title and not content:
            return jsonify({'error': 'Title or content required'}), 400
        
        tags = generate_tags(title, content, max_tags)
        
        return jsonify({
            'success': True,
            'tags': tags
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """
    Summarize note content
    POST body: {"content": "...", "max_length": 100}
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        max_length = data.get('max_length', 100)
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        summary = summarize_note(content, max_length)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-note', methods=['POST'])
def api_generate_note():
    """
    Generate a complete note from natural language description
    POST body: {"description": "...", "language": "English"}
    """
    try:
        data = request.get_json()
        description = data.get('description', '')
        language = data.get('language', 'English')
        
        if not description:
            return jsonify({'error': 'No description provided'}), 400
        
        # Create prompt for generating structured note
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant that creates well-structured notes from natural language descriptions.
Generate a note in {language} with the following structure:
1. A clear, concise title (one line)
2. Well-organized content with proper formatting
3. Suggest 3-5 relevant tags (comma-separated)

Format your response as JSON with this exact structure:
{{
    "title": "Note title here",
    "content": "Detailed content here with proper formatting and line breaks",
    "tags": "tag1, tag2, tag3"
}}

Make the content clear, organized, and useful. Use bullet points or numbered lists when appropriate."""
            },
            {
                "role": "user",
                "content": f"Create a note about: {description}"
            }
        ]
        
        from backend.llm import call_llm_model
        import json
        
        response_text = call_llm_model(messages, temperature=0.7)
        
        # Try to parse JSON response
        try:
            # Find JSON in the response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                note_data = json.loads(json_str)
            else:
                # Fallback: create structure from raw response
                lines = response_text.strip().split('\n')
                note_data = {
                    'title': lines[0] if lines else 'Generated Note',
                    'content': '\n'.join(lines[1:]) if len(lines) > 1 else response_text,
                    'tags': ''
                }
        except:
            # Fallback: use raw response
            note_data = {
                'title': 'Generated Note',
                'content': response_text,
                'tags': ''
            }
        
        return jsonify({
            'success': True,
            'note': note_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

