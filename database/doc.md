# Note Taking App - Database Directory

This folder contains the SQLite database file for the application.

## Database File

- `notes.db` - SQLite database file (auto-generated on first run)

## Schema

The database contains a single table:

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Note

The `notes.db` file is excluded from version control via `.gitignore` to avoid committing user data.
