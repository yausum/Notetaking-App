# LLM API Documentation

## Overview
This document describes the LLM-powered API endpoints available in the Note Taking App.

---

## API Endpoints

### 1. Translate Text

**Endpoint:** `POST /api/translate`

**Description:** Translate text to a target language using AI.

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "target_language": "Chinese"
}
```

**Response:**
```json
{
  "success": true,
  "original": "Hello, how are you?",
  "translated": "你好，你好嗎？",
  "target_language": "Chinese"
}
```

**Supported Languages:**
- Chinese (中文)
- English
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Japanese (日本語)
- Korean (한국어)
- And many more...

**Example Usage:**
```javascript
const response = await fetch('/api/translate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'Hello world',
        target_language: 'Chinese'
    })
});

const data = await response.json();
console.log(data.translated); // "你好世界"
```

---

### 2. Generate Tags

**Endpoint:** `POST /api/generate-tags`

**Description:** Automatically generate relevant tags based on note title and content.

**Request Body:**
```json
{
  "title": "Python Machine Learning Tutorial",
  "content": "This note covers basic machine learning concepts using Python and scikit-learn library.",
  "max_tags": 5
}
```

**Response:**
```json
{
  "success": true,
  "tags": "Python, Machine Learning, Tutorial, scikit-learn, AI"
}
```

**Example Usage:**
```javascript
const response = await fetch('/api/generate-tags', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        title: 'Meeting Notes',
        content: 'Discussed Q1 budget and marketing strategy',
        max_tags: 3
    })
});

const data = await response.json();
console.log(data.tags); // "Meeting, Budget, Marketing"
```

---

### 3. Summarize Note

**Endpoint:** `POST /api/summarize`

**Description:** Generate a concise summary of note content.

**Request Body:**
```json
{
  "content": "Long text content here...",
  "max_length": 100
}
```

**Response:**
```json
{
  "success": true,
  "summary": "Brief summary of the content in approximately 100 words or less."
}
```

**Example Usage:**
```javascript
const response = await fetch('/api/summarize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        content: 'Very long article text...',
        max_length: 50
    })
});

const data = await response.json();
console.log(data.summary);
```

---

## Error Handling

All endpoints return errors in the following format:

**Error Response:**
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing required fields)
- `500` - Internal Server Error (API failure)

**Example Error:**
```json
{
  "success": false,
  "error": "No text provided"
}
```

---

## Testing with cURL

### Translate
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "target_language": "Chinese"}'
```

### Generate Tags
```bash
curl -X POST http://localhost:5000/api/generate-tags \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Tutorial", "content": "Learn Python basics", "max_tags": 3}'
```

### Summarize
```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"content": "Long text here...", "max_length": 50}'
```

---

## Rate Limits

GitHub Models API has usage limits:
- Free tier: Limited requests per day
- Rate limiting: Automatic retry after cooldown
- Token limits: ~4000 tokens per request

---

## UI Integration

### View Note Page
- **Translate Button**: Click "🌐 Translate" to translate the entire note
- **Language Selection**: Choose from popular languages or enter custom language
- **Translation Display**: Results shown in a purple gradient box below the note

### Add/Edit Note Page
- **Generate Tags Button**: Click "✨ Generate" next to tags field
- **Auto-fill**: AI suggests relevant tags based on title and content
- **Manual Override**: You can edit or replace generated tags

---

## Tips for Best Results

### Translation
- Longer text generally translates better
- Specify language clearly (e.g., "Traditional Chinese" vs "Simplified Chinese")
- Technical terms may not translate perfectly

### Tag Generation
- More descriptive titles and content = better tags
- Works best with at least 2-3 sentences
- Generates 5 tags by default, can be adjusted

### Summarization
- Best for content longer than 100 words
- Specify max_length based on your needs
- Preserves key information and main ideas

---

## Troubleshooting

### "API token not found"
- Ensure `.env` file exists with `GITHUB_TOKEN`
- Check token is valid at https://github.com/settings/tokens

### "401 Unauthorized"
- Token may be expired or lack required permissions
- Regenerate token with proper scopes

### "Translation failed"
- Check internet connection
- Verify API endpoint is accessible
- May have hit rate limits (wait and retry)

---

## Future Enhancements

Planned features:
- ✨ Improve note content (grammar and clarity)
- 🤖 AI chat for notes (ask questions about your notes)
- 📊 Sentiment analysis
- 🔍 Semantic search
- 📝 Auto-completion suggestions

---

## Support

For issues or questions:
1. Check this documentation
2. Review `LLM_SETUP_GUIDE.md`
3. Test with `python backend/llm.py`
4. Check Flask console for error messages
