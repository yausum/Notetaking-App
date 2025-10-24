# Sorting Feature Documentation

## 📊 Overview

A comprehensive sorting system has been added to the Note Taking App, allowing users to organize notes by multiple criteria.

## ✨ Features

### Sorting Options

1. **Last Updated** (Default)
   - Sorts notes by most recently updated
   - Shows newest changes first

2. **Created Date**
   - Sorts by creation date
   - Newest notes appear first

3. **Title (A-Z)**
   - Alphabetical sorting by note title
   - Case-insensitive

4. **Event Date**
   - Sorts by event date
   - Notes with event dates appear first
   - Notes without dates appear last

5. **Event Time**
   - Sorts by event time
   - Notes with times appear first
   - Notes without times appear last

## 🎯 Where Sorting is Available

### 1. Homepage (All Notes)
- Dropdown selector in page header
- Auto-submits when selection changes
- Persists across page refreshes

### 2. Search Results
- Dropdown selector below search bar
- Works with search query
- Maintains search term when sorting

### 3. Global Search Bar
- Integrated dropdown in search bar
- Available on all pages
- Applies when searching

## 💻 Implementation Details

### Backend (`backend/app.py`)

#### Index Route
```python
@app.route('/')
def index():
    sort_by = request.args.get('sort', 'updated')
    
    # Different SQL queries based on sort option
    if sort_by == 'event_date':
        # NULL values appear last
        notes = conn.execute(
            'SELECT * FROM notes ORDER BY CASE WHEN event_date IS NULL THEN 1 ELSE 0 END, 
             event_date DESC, event_time DESC'
        ).fetchall()
```

#### Search Route
```python
@app.route('/search')
def search():
    query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'updated')
    
    # Combines search with sorting
    base_query = 'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ...'
    order_clause = ' ORDER BY ...'  # Based on sort_by
```

### SQL Ordering

**Handling NULL Values:**
```sql
-- Event date sorting (NULL last)
ORDER BY 
    CASE WHEN event_date IS NULL THEN 1 ELSE 0 END,
    event_date DESC,
    event_time DESC

-- Event time sorting (NULL last)
ORDER BY 
    CASE WHEN event_time IS NULL THEN 1 ELSE 0 END,
    event_time DESC,
    event_date DESC
```

### Frontend

#### Base Template (`base.html`)
```html
<select name="sort" class="sort-select">
    <option value="updated" {% if request.args.get('sort', 'updated') == 'updated' %}selected{% endif %}>
        Sort: Last Updated
    </option>
    <option value="event_date">Sort: Event Date</option>
    <!-- More options -->
</select>
```

#### Index Template (`index.html`)
```html
<div class="sort-controls">
    <form method="GET" action="{{ url_for('index') }}" class="sort-form">
        <label for="sort">Sort by:</label>
        <select name="sort" id="sort" class="sort-select" onchange="this.form.submit()">
            <!-- Options -->
        </select>
    </form>
</div>
```

#### Search Template (`search.html`)
```html
<form method="GET" action="{{ url_for('search') }}" class="sort-form">
    <input type="hidden" name="q" value="{{ query }}">
    <select name="sort" id="sort" class="sort-select" onchange="this.form.submit()">
        <!-- Options -->
    </select>
</form>
```

### CSS Styling (`style.css`)

#### Sort Select Styling
```css
.sort-select {
    padding: 0.75rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 0.95rem;
    background-color: white;
    min-width: 180px;
    cursor: pointer;
}

.sort-select:hover {
    border-color: var(--primary-color);
}
```

#### Layout Components
```css
.page-header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sort-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.sort-form {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
```

## 📱 Responsive Design

### Mobile Adaptations

- Sort controls stack vertically
- Full-width dropdowns on small screens
- Centered alignment
- Touch-friendly spacing

```css
@media (max-width: 768px) {
    .page-header-content {
        flex-direction: column;
        text-align: center;
    }
    
    .sort-controls {
        width: 100%;
        justify-content: center;
    }
}
```

## 🎨 User Experience

### Auto-Submit Behavior

```javascript
<select onchange="this.form.submit()">
```

- Immediate sorting on selection change
- No extra "Apply" button needed
- Smooth page refresh

### State Persistence

- Sort preference maintained via URL parameters
- Works with browser back/forward buttons
- Shareable URLs with sort state

### Visual Feedback

- Hover effects on dropdowns
- Selected option highlighted
- Focus states for accessibility

## 🔄 Sort Logic

### Priority Order

**Event Date Sort:**
1. Notes with event dates (newest first)
2. Secondary sort by event time
3. Notes without event dates (last)

**Event Time Sort:**
1. Notes with event times (latest first)
2. Secondary sort by event date
3. Notes without event times (last)

### NULL Handling

```sql
CASE WHEN event_date IS NULL THEN 1 ELSE 0 END
```

This ensures:
- Non-NULL values have priority (0)
- NULL values go last (1)

## 📊 Use Cases

### 1. Event Planning
- Sort by event date to see upcoming events
- Sort by event time for daily scheduling

### 2. Content Management
- Sort by created date to find oldest notes
- Sort by title for alphabetical reference

### 3. Recent Work
- Sort by updated to see recent changes
- Default view shows latest activity

### 4. Search + Sort
- Search for "meeting"
- Sort results by event date
- Find upcoming meetings

## 🚀 Performance

### Optimization
- Simple SQL ORDER BY clauses
- Indexed timestamp columns
- Efficient NULL handling
- No JavaScript sorting (server-side)

### Query Examples

```sql
-- Fast with indexes
SELECT * FROM notes ORDER BY updated_at DESC

-- Efficient NULL handling
SELECT * FROM notes 
ORDER BY CASE WHEN event_date IS NULL THEN 1 ELSE 0 END, 
         event_date DESC
```

## 🧪 Testing

### Test Scenarios

1. ✅ Sort homepage by each option
2. ✅ Sort search results
3. ✅ Combine search + sort
4. ✅ Mobile responsive layout
5. ✅ NULL values handled correctly
6. ✅ URL parameters persist
7. ✅ Auto-submit works

## 🔮 Future Enhancements

Potential improvements:
- Custom sort orders (ascending/descending toggle)
- Save user's preferred sort option
- Multi-level sorting
- Sort by tag count
- Sort by content length
- Visual sort direction indicators

## 📋 Summary

The sorting feature provides:
- ✅ 5 sorting options
- ✅ Available in 3 locations
- ✅ Server-side sorting
- ✅ NULL-safe queries
- ✅ Responsive design
- ✅ Auto-submit UX
- ✅ State persistence

---

**Status**: ✅ Fully implemented and tested
**Version**: v1.1 - Sorting Feature
**Date**: October 24, 2025
