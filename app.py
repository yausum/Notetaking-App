from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DATABASE = 'notes.db'

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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('add_note'))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO notes (title, content, category) VALUES (?, ?, ?)',
                     (title, content, category))
        conn.commit()
        conn.close()
        
        flash('Note added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_note.html')

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
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('edit_note', id=id))
        
        conn.execute('UPDATE notes SET title = ?, content = ?, category = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                     (title, content, category, id))
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
    
    if query:
        conn = get_db_connection()
        notes = conn.execute(
            'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR category LIKE ? ORDER BY updated_at DESC',
            (f'%{query}%', f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
    else:
        notes = []
    
    return render_template('search.html', notes=notes, query=query)

@app.route('/api/notes')
def api_notes():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(note) for note in notes])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
