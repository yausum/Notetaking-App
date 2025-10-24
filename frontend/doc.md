# Frontend - User Interface

This folder contains all frontend assets for the Note Taking App.

## Structure

```
frontend/
├── templates/          # HTML templates (Jinja2)
│   ├── base.html      # Base template with common layout
│   ├── index.html     # Homepage (all notes)
│   ├── add_note.html  # Create new note form
│   ├── edit_note.html # Edit existing note form
│   ├── view_note.html # View single note
│   └── search.html    # Search results page
└── static/            # Static assets (CSS, JS, images)
    ├── style.css      # Application styling
    └── script.js      # JavaScript interactions
```

## Templates

All templates use **Jinja2** templating engine and inherit from `base.html` for consistent layout.

### Template Inheritance Example

```html
{% extends "base.html" %}

{% block title %}My Page Title{% endblock %}

{% block content %}
  <h1>My Content</h1>
{% endblock %}
```

## Static Files

- **style.css** - Complete styling with responsive design
- **script.js** - Client-side interactions and keyboard shortcuts

## Features

- ✅ Responsive design (mobile-friendly)
- ✅ Card-based layout
- ✅ Hover animations
- ✅ Auto-hiding flash messages
- ✅ Keyboard shortcuts (Ctrl+K, Ctrl+N)
- ✅ Form validation
- ✅ Character counter
