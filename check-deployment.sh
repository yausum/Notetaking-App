#!/usr/bin/env bash
# Quick verification script before Vercel deployment

echo "=========================================="
echo "🔍 Pre-Deployment Checklist"
echo "=========================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✅ .env file exists"
    echo "   (Make sure it's in .gitignore!)"
else
    echo "❌ .env file not found"
fi

# Check if .gitignore contains .env
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "✅ .env is in .gitignore"
else
    echo "⚠️  Warning: .env not found in .gitignore"
fi

# Check required files
echo ""
echo "📁 Required Files:"
files=("vercel.json" "requirements.txt" "run.py" "backend/app.py" "backend/llm.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file missing"
    fi
done

echo ""
echo "=========================================="
echo "📝 Next Steps:"
echo "=========================================="
echo "1. Run this in Supabase SQL Editor:"
echo "   (Dashboard → SQL Editor → New Query)"
echo ""
echo "   CREATE TABLE IF NOT EXISTS notes ("
echo "       id SERIAL PRIMARY KEY,"
echo "       title TEXT NOT NULL,"
echo "       content TEXT NOT NULL,"
echo "       category TEXT,"
echo "       tags TEXT,"
echo "       event_date DATE,"
echo "       event_time TIME,"
echo "       created_at TIMESTAMP DEFAULT NOW(),"
echo "       updated_at TIMESTAMP DEFAULT NOW()"
echo "   );"
echo ""
echo "2. Push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for Vercel deployment'"
echo "   git push origin main"
echo ""
echo "3. Deploy on Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Import your GitHub repo"
echo "   - Add environment variables"
echo "   - Deploy!"
echo ""
echo "=========================================="
