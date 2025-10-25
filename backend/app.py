from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from supabase import create_client, Client
from datetime import datetime
import os
from dotenv import load_dotenv
from backend.llm import translate_text, generate_tags, summarize_note

# Load environment variables
load_dotenv()

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure Flask to use frontend folder for templates and static files
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'frontend', 'static'),
            static_url_path='/static')
app.secret_key = 'your-secret-key-here'

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Explicitly serve static files for Vercel
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images)"""
    static_dir = os.path.join(BASE_DIR, 'frontend', 'static')
    return send_from_directory(static_dir, filename)

def init_db():
    """Initialize the Supabase database with the notes table"""
    try:
        # Check if table exists by trying to select from it
        result = supabase.table('notes').select("id").limit(1).execute()
        print("✓ Notes table already exists")
    except Exception as e:
        print(f"Note: Table might not exist yet. Please run init_supabase.py first.")
        print(f"Error: {e}")

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'updated')
    
    try:
        # Determine sort order
        if sort_by == 'event_date':
            # Sort by event date, putting NULL values last using NULLS LAST
            query = supabase.table('notes').select('*').order('event_date', desc=False, nullsfirst=False).order('event_time', desc=False)
        elif sort_by == 'event_time':
            # Sort by event time, putting NULL values last
            query = supabase.table('notes').select('*').order('event_time', desc=False, nullsfirst=False).order('event_date', desc=False)
        elif sort_by == 'created':
            query = supabase.table('notes').select('*').order('created_at', desc=True)
        elif sort_by == 'title':
            query = supabase.table('notes').select('*').order('title', desc=False)
        else:  # default: updated
            query = supabase.table('notes').select('*').order('updated_at', desc=True)
        
        response = query.execute()
        notes = response.data
        
    except Exception as e:
        print(f"Error fetching notes: {e}")
        notes = []
        flash('Error loading notes', 'error')
    
    return render_template('index.html', notes=notes, sort_by=sort_by)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        tags = request.form.get('tags', '')
        event_date = request.form.get('event_date', None)
        event_time = request.form.get('event_time', None)
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('add_note'))
        
        # Convert empty strings to None for NULL in database
        event_date = event_date if event_date else None
        event_time = event_time if event_time else None
        
        try:
            response = supabase.table('notes').insert({
                'title': title,
                'content': content,
                'category': category,
                'tags': tags,
                'event_date': event_date,
                'event_time': event_time
            }).execute()
            
            note_id = response.data[0]['id'] if response.data else None
            
            # Check if this is from generate page (AJAX request)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'note_id': note_id})
            
            flash('Note added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Error adding note: {e}")
            flash('Error adding note', 'error')
            return redirect(url_for('add_note'))
    
    return render_template('add_note.html')

@app.route('/generate')
def generate_note():
    return render_template('generate_note.html')

@app.route('/note/<int:id>')
def view_note(id):
    try:
        response = supabase.table('notes').select('*').eq('id', id).execute()
        note = response.data[0] if response.data else None
        
        if note is None:
            flash('Note not found!', 'error')
            return redirect(url_for('index'))
        
        return render_template('view_note.html', note=note)
        
    except Exception as e:
        print(f"Error fetching note: {e}")
        flash('Error loading note', 'error')
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    try:
        response = supabase.table('notes').select('*').eq('id', id).execute()
        note = response.data[0] if response.data else None
        
        if note is None:
            flash('Note not found!', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            category = request.form.get('category', '')
            tags = request.form.get('tags', '')
            event_date = request.form.get('event_date', None)
            event_time = request.form.get('event_time', None)
            
            if not title or not content:
                flash('Title and content are required!', 'error')
                return redirect(url_for('edit_note', id=id))
            
            # Convert empty strings to None for NULL in database
            event_date = event_date if event_date else None
            event_time = event_time if event_time else None
            
            try:
                supabase.table('notes').update({
                    'title': title,
                    'content': content,
                    'category': category,
                    'tags': tags,
                    'event_date': event_date,
                    'event_time': event_time,
                    'updated_at': datetime.now().isoformat()
                }).eq('id', id).execute()
                
                flash('Note updated successfully!', 'success')
                return redirect(url_for('view_note', id=id))
                
            except Exception as e:
                print(f"Error updating note: {e}")
                flash('Error updating note', 'error')
                return redirect(url_for('edit_note', id=id))
        
        return render_template('edit_note.html', note=note)
        
    except Exception as e:
        print(f"Error loading note: {e}")
        flash('Error loading note', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    try:
        supabase.table('notes').delete().eq('id', id).execute()
        flash('Note deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting note: {e}")
        flash('Error deleting note', 'error')
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'updated')
    
    if query:
        try:
            # Build the search query - Supabase supports multiple OR conditions
            base_query = supabase.table('notes').select('*')
            
            # Use Supabase's textSearch or ilike for pattern matching
            # We'll use ilike (case-insensitive LIKE) for each field
            search_query = base_query.or_(
                f"title.ilike.%{query}%,content.ilike.%{query}%,category.ilike.%{query}%,tags.ilike.%{query}%"
            )
            
            # Add sorting
            if sort_by == 'event_date':
                search_query = search_query.order('event_date', desc=True, nulls_first=False).order('event_time', desc=True)
            elif sort_by == 'event_time':
                search_query = search_query.order('event_time', desc=True, nulls_first=False).order('event_date', desc=True)
            elif sort_by == 'created':
                search_query = search_query.order('created_at', desc=True)
            elif sort_by == 'title':
                search_query = search_query.order('title', desc=False)
            else:  # default: updated
                search_query = search_query.order('updated_at', desc=True)
            
            response = search_query.execute()
            notes = response.data
            
        except Exception as e:
            print(f"Error searching notes: {e}")
            notes = []
            flash('Error searching notes', 'error')
    else:
        notes = []
    
    return render_template('search.html', notes=notes, query=query, sort_by=sort_by)

@app.route('/api/notes')
def api_notes():
    try:
        response = supabase.table('notes').select('*').order('updated_at', desc=True).execute()
        notes = response.data
        return jsonify(notes)
    except Exception as e:
        print(f"Error fetching notes API: {e}")
        return jsonify({'error': 'Failed to fetch notes'}), 500

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
        
        # System prompt as specified with date and time extraction
        system_prompt = f"""Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Category: A single category that best describes the note (e.g., Work, Personal, Study, Health, Finance, Travel, Shopping, Ideas, etc.)
4. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes.
5. EventDate (optional): Extract date if mentioned (format: YYYY-MM-DD). Use null if not available.
6. EventTime (optional): Extract time if mentioned (format: HH:MM in 24-hour). Use null if not available.
Output in JSON format without ```json. Output title and notes in the language: {language}.

Date parsing rules:
- "tomorrow" = next day
- "next Monday/Tuesday/etc" = next occurrence of that day
- "Jan 15", "15 Jan", "January 15" = current year if not specified
- If only day mentioned (e.g., "Friday"), use next occurrence

Time parsing rules:
- "5pm" = "17:00"
- "9am" = "09:00"
- "noon" = "12:00"
- "midnight" = "00:00"

Category suggestions:
- Work: meetings, projects, deadlines, tasks
- Personal: appointments, reminders, personal tasks
- Study: homework, exams, research, learning
- Health: exercise, doctor appointments, medication
- Finance: bills, budgets, expenses
- Travel: trips, bookings, itineraries
- Shopping: grocery lists, purchases
- Ideas: brainstorming, creative thoughts

Example:
Input: "Badminton tmr 5pm @polyu".
Output:
{{
"Title": "Badminton at PolyU",
"Notes": "Remember to play badminton at 5pm tomorrow at PolyU.",
"Category": "Personal",
"Tags": ["badminton", "sports"],
"EventDate": "2025-10-25",
"EventTime": "17:00"
}}

Example without date/time:
Input: "Buy milk and eggs".
Output:
{{
"Title": "Shopping List",
"Notes": "Remember to buy milk and eggs.",
"Category": "Shopping",
"Tags": ["shopping", "groceries"],
"EventDate": null,
"EventTime": null
}}"""
        
        # Create messages for LLM
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": description
            }
        ]
        
        from backend.llm import call_llm_model
        import json
        
        response_text = call_llm_model(messages, temperature=0.3)
        
        # Try to parse JSON response
        try:
            # Find JSON in the response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                note_data_raw = json.loads(json_str)
                
                # Convert to our database format
                # Expected keys: Title, Notes, Category, Tags (array), EventDate, EventTime
                title = note_data_raw.get('Title', note_data_raw.get('title', 'Generated Note'))
                notes = note_data_raw.get('Notes', note_data_raw.get('notes', note_data_raw.get('content', '')))
                category = note_data_raw.get('Category', note_data_raw.get('category', ''))
                tags = note_data_raw.get('Tags', note_data_raw.get('tags', []))
                event_date = note_data_raw.get('EventDate', note_data_raw.get('event_date', None))
                event_time = note_data_raw.get('EventTime', note_data_raw.get('event_time', None))
                
                # Convert tags array to comma-separated string
                if isinstance(tags, list):
                    tags_str = ', '.join(tags)
                else:
                    tags_str = str(tags)
                
                # Handle null values for date/time
                if event_date == 'null' or event_date == '':
                    event_date = None
                if event_time == 'null' or event_time == '':
                    event_time = None
                
                note_data = {
                    'title': title,
                    'content': notes,
                    'category': category,
                    'tags': tags_str,
                    'event_date': event_date,
                    'event_time': event_time
                }
            else:
                # Fallback: create structure from raw response
                lines = response_text.strip().split('\n')
                note_data = {
                    'title': lines[0] if lines else 'Generated Note',
                    'content': '\n'.join(lines[1:]) if len(lines) > 1 else response_text,
                    'category': '',
                    'tags': '',
                    'event_date': None,
                    'event_time': None
                }
        except:
            # Fallback: use raw response
            note_data = {
                'title': 'Generated Note',
                'content': response_text,
                'category': '',
                'tags': '',
                'event_date': None,
                'event_time': None
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

