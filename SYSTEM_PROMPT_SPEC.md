# 🤖 AI Generate Note - System Prompt Specification

## 📋 Overview

The AI Generate Note feature now uses a structured extraction approach that converts natural language input into properly formatted notes.

---

## 🎯 System Prompt

```
Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes.
Output in JSON format without ```json. Output title and notes in the language: {lang}.

Example:
Input: "Badminton tmr 5pm @polyu".
Output:
{
  "Title": "Badminton at PolyU",
  "Notes": "Remember to play badminton at 5pm tomorrow at PolyU.",
  "Tags": ["badminton", "sports"]
}
```

---

## 🔧 Technical Implementation

### Backend Processing

**API Endpoint:** `POST /api/generate-note`

**Request:**
```json
{
  "description": "Badminton tmr 5pm @polyu",
  "language": "English"
}
```

**LLM Processing:**
1. System prompt with language specification
2. User input as-is (no "Create a note about:" prefix)
3. Temperature: 0.3 (for consistent, focused output)
4. JSON extraction from response

**Response Mapping:**
- `Title` → `title` (database field)
- `Notes` → `content` (database field)
- `Tags` (array) → `tags` (comma-separated string)

**Response:**
```json
{
  "success": true,
  "note": {
    "title": "Badminton at PolyU",
    "content": "Remember to play badminton at 5pm tomorrow at PolyU.",
    "tags": "badminton, sports"
  }
}
```

---

## 📊 Field Specifications

### Title
- **Constraint:** Less than 5 words
- **Format:** Concise, descriptive
- **Example:** "Badminton at PolyU"
- **Language:** Matches output language setting

### Notes (Content)
- **Format:** Full sentences
- **Style:** Complete, well-written
- **Expansion:** Converts shorthand to complete thoughts
- **Example:** "tmr 5pm" → "at 5pm tomorrow"
- **Language:** Matches output language setting

### Tags
- **Type:** Array in JSON
- **Constraint:** At most 3 tags
- **Format:** Single keywords or short phrases
- **Stored as:** Comma-separated string in database
- **Example:** `["badminton", "sports"]` → `"badminton, sports"`

---

## 💡 Input → Output Examples

### Example 1: Simple Event
**Input:**
```
"Badminton tmr 5pm @polyu"
Language: English
```

**Output:**
```json
{
  "Title": "Badminton at PolyU",
  "Notes": "Remember to play badminton at 5pm tomorrow at PolyU.",
  "Tags": ["badminton", "sports"]
}
```

### Example 2: Shopping List
**Input:**
```
"Buy milk eggs bread at supermarket"
Language: English
```

**Output:**
```json
{
  "Title": "Supermarket Shopping",
  "Notes": "Remember to buy milk, eggs, and bread at the supermarket.",
  "Tags": ["shopping", "groceries"]
}
```

### Example 3: Meeting Note
**Input:**
```
"Meeting with John about Q1 budget on Friday"
Language: English
```

**Output:**
```json
{
  "Title": "Q1 Budget Meeting",
  "Notes": "Schedule a meeting with John on Friday to discuss the Q1 budget.",
  "Tags": ["meeting", "budget", "Q1"]
}
```

### Example 4: Multilingual (Chinese)
**Input:**
```
"Dentist appointment next Tuesday 3pm"
Language: Chinese
```

**Output:**
```json
{
  "Title": "牙醫預約",
  "Notes": "下週二下午3點記得去看牙醫。",
  "Tags": ["牙醫", "預約"]
}
```

### Example 5: Workout Plan
**Input:**
```
"Gym workout 6am Monday chest and arms"
Language: English
```

**Output:**
```json
{
  "Title": "Monday Gym Workout",
  "Notes": "Go to the gym on Monday at 6am for a chest and arms workout.",
  "Tags": ["gym", "workout", "fitness"]
}
```

---

## 🎨 UI Changes

### Input Section
- **Placeholder:** Shows examples with shorthand format
- **Help Text:** "Be brief and natural. AI will extract and structure it..."
- **Examples Box:** 4 sample inputs demonstrating the format

### Preview Section
- **Title Field:** Shows concise title (< 5 words)
- **Content Area:** Shows expanded full sentences
- **Tags Label:** Now shows "(max 3)" reminder
- **Tags Display:** Maximum 3 tag badges

---

## 🔍 Key Differences from Previous Version

| Aspect | Previous | New |
|--------|----------|-----|
| **Title Length** | Variable | < 5 words |
| **Content Style** | "Create a note about:" | Direct extraction |
| **Tags Count** | 3-5 tags | Max 3 tags |
| **Input Style** | Descriptive prompt | Natural shorthand |
| **Temperature** | 0.7 | 0.3 |
| **Prompt Type** | Generation | Extraction |
| **Tags Format** | Comma-string | Array → comma-string |

---

## 🚀 Usage Guidelines

### ✅ Good Input Examples
```
✓ "Badminton tmr 5pm @polyu"
✓ "Buy milk eggs bread"
✓ "Meeting John Friday Q1 budget"
✓ "Dentist Tuesday 3pm"
✓ "Gym 6am Monday chest arms"
```

### ❌ Not Recommended
```
✗ "I need to remember to play badminton..." (too verbose)
✗ "Create a note about meeting" (instructional format)
✗ "" (empty input)
```

---

## 🔧 Code Walkthrough

### Backend (app.py)

```python
# System prompt with language variable
system_prompt = f"""Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes.
Output in JSON format without ```json. Output title and notes in the language: {language}.
..."""

# Messages array
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": description}  # Direct input
]

# Call LLM with lower temperature for consistency
response_text = call_llm_model(messages, temperature=0.3)

# Parse JSON and map fields
note_data_raw = json.loads(json_str)
title = note_data_raw.get('Title', note_data_raw.get('title', 'Generated Note'))
notes = note_data_raw.get('Notes', note_data_raw.get('notes', ''))
tags = note_data_raw.get('Tags', note_data_raw.get('tags', []))

# Convert tags array to string
if isinstance(tags, list):
    tags_str = ', '.join(tags)
```

### Frontend (generate_note.html)

```javascript
// Request body sends direct description
body: JSON.stringify({
    description: description,  // No "Create a note about:" prefix
    language: language
})

// Response handling remains the same
// Tags are already comma-separated from backend
```

---

## 📊 Benefits of New Approach

### 1. **Concise Titles**
- Enforces < 5 words constraint
- More scannable in note lists
- Better for mobile displays

### 2. **Natural Input**
- Users can type shorthand
- Less typing required
- Matches how people naturally jot notes

### 3. **Consistent Tags**
- Always max 3 tags
- Prevents tag bloat
- More focused categorization

### 4. **Full Sentences**
- AI expands shorthand
- More readable content
- Professional formatting

### 5. **Extraction vs Generation**
- More accurate to user intent
- Less hallucination
- Faster processing

---

## 🧪 Testing Examples

### Test Case 1: Event with Location
```
Input: "Team lunch tomorrow noon @Italian restaurant"
Expected Title: "Team Lunch Tomorrow"
Expected Content: "Remember to attend the team lunch at noon tomorrow at the Italian restaurant."
Expected Tags: ["lunch", "team", "restaurant"]
```

### Test Case 2: Task List
```
Input: "Fix bug in login page, update documentation, deploy to staging"
Expected Title: "Development Tasks"
Expected Content: "Complete the following tasks: fix the bug in the login page, update the documentation, and deploy to staging."
Expected Tags: ["development", "tasks", "bug"]
```

### Test Case 3: Personal Reminder
```
Input: "Call mom birthday gift ideas"
Expected Title: "Call Mom"
Expected Content: "Remember to call mom to discuss birthday gift ideas."
Expected Tags: ["personal", "birthday", "family"]
```

---

## 🎯 Summary

The updated AI Generate Note feature:
- ✅ Uses extraction-based approach
- ✅ Enforces 5-word title limit
- ✅ Converts shorthand to full sentences
- ✅ Limits to 3 tags maximum
- ✅ Accepts natural, brief input
- ✅ Supports multilingual output
- ✅ More consistent results (temperature 0.3)

**User Experience:**
Type natural shorthand → AI extracts and structures → Preview → Save → Edit

**Perfect for:** Quick capture, event reminders, task lists, appointments, shopping lists, and any brief note-taking scenarios.

---

🚀 **Now Live:** http://localhost:5000/generate
