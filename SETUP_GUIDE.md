# 🚀 Quick Setup Guide - Supabase PostgreSQL

This guide will help you set up the Note-Taking App with Supabase PostgreSQL in under 5 minutes.

## Step 1: Create Supabase Project (2 minutes)

1. Go to [supabase.com](https://supabase.com) and sign in (or create free account)
2. Click **"New Project"**
3. Fill in:
   - **Project Name**: `notetaking-app` (or any name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to you
4. Click **"Create new project"** and wait ~2 minutes for setup

## Step 2: Get Database Connection String (1 minute)

1. In your Supabase project dashboard, go to **Project Settings** (⚙️ icon in sidebar)
2. Click **"Database"** in the left menu
3. Scroll down to **"Connection pooling"** section
4. **Mode**: Select **"Transaction"**
5. **Connection string**: Click to reveal and copy the full URI
   
   It looks like:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
   ```

6. **Important**: Replace `[YOUR-PASSWORD]` with your actual database password (from Step 1)

## Step 3: Update Your .env File (30 seconds)

Open `.env` file in your project root and update:

```env
# GitHub Models API (keep your existing token)
GITHUB_TOKEN=your_existing_github_token
OPENAI_MODEL=openai/gpt-4.1-mini

# Supabase PostgreSQL - UPDATE THIS LINE
DATABASE_URL=postgresql://postgres.xxxxx:YOUR-PASSWORD@aws-0-region.pooler.supabase.com:6543/postgres
```

**Replace the entire `DATABASE_URL` line** with the connection string from Step 2.

## Step 4: Install Dependencies (1 minute)

Open terminal/PowerShell in project directory:

```bash
pip install -r requirements.txt
```

This installs `psycopg2-binary` (PostgreSQL adapter) and other dependencies.

## Step 5: Initialize Database (30 seconds)

Run the initialization script:

```bash
python init_supabase.py
```

✅ Expected output:
```
==================================================
Supabase PostgreSQL Database Initialization
==================================================
Connecting to Supabase PostgreSQL...
Creating notes table...
Creating indexes...
✓ Database initialized successfully!
✓ Notes table created
✓ Indexes created
```

## Step 6: Launch App (10 seconds)

```bash
python run.py
```

Open browser: http://localhost:5000

🎉 **Done! Your app is now running with Supabase PostgreSQL!**

---

## 🔍 Verify Setup

### Check Database in Supabase Dashboard

1. Go to **Table Editor** in Supabase sidebar
2. You should see a `notes` table
3. Click on it to view structure (columns: id, title, content, etc.)

### Test Create Note

1. In your app, click **"Add New Note"**
2. Fill in title and content
3. Click **"Save Note"**
4. Go back to Supabase > Table Editor > `notes` table
5. Click **"Refresh"** - you should see your note!

---

## ⚠️ Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'psycopg2'"

**Solution**: Install the package
```bash
pip install psycopg2-binary
```

### Problem: "connection refused" or "could not connect to server"

**Solution**: Check your `.env` file:
1. Make sure `DATABASE_URL` has NO spaces around the `=`
2. Verify the password is correct (no special characters unescaped)
3. Test connection string in Supabase dashboard first

### Problem: "password authentication failed"

**Solution**: 
1. Get fresh connection string from Supabase (Project Settings > Database)
2. Make sure you replaced `[YOUR-PASSWORD]` with actual password
3. Password should NOT be in brackets

### Problem: init_supabase.py shows "Import error"

**Solution**: Make sure you're in the correct directory
```bash
cd Notetaking-App
python init_supabase.py
```

---

## 📊 What Changed from SQLite?

| SQLite | Supabase PostgreSQL |
|--------|---------------------|
| Local file `notes.db` | Cloud-hosted database |
| Single user | Multi-user capable |
| Limited to 2TB | Unlimited* storage |
| No backup | Automatic daily backups |
| Manual scaling | Auto-scales |

*Free tier: 500MB database, 2GB bandwidth/month (plenty for personal use!)

---

## 🎁 Bonus: Supabase Features to Explore

After basic setup works, explore these:

### Real-time Subscriptions
Get live updates when notes change across multiple devices.

### Row Level Security (RLS)
Add user authentication and make notes private per user.

### Storage
Upload and attach files/images to your notes.

### Edge Functions
Run serverless functions for advanced AI processing.

### SQL Editor
Write custom queries and analytics in the Supabase dashboard.

---

## 🔗 Useful Links

- **Supabase Dashboard**: https://app.supabase.com
- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Migration Guide**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **API Docs**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 💡 Tips

1. **Free Tier Limits**: 
   - 500MB database storage
   - 2 free projects
   - Auto-pauses after 7 days of inactivity (just visit dashboard to wake up)

2. **Connection Pooling**: 
   - Always use the "Transaction" mode connection string (port 6543)
   - Don't use "Session" mode (port 5432) - it's for direct connections

3. **Backup**: 
   - Free tier has automatic daily backups
   - Download dumps from Project Settings > Database > Backups

4. **Security**:
   - Never commit `.env` file to git
   - Rotate passwords if exposed
   - Use environment variables in production (Vercel, Heroku, etc.)

---

**Setup Time**: ~5 minutes  
**Difficulty**: ⭐⭐☆☆☆ (Easy)  
**Status**: ✅ Production-ready
