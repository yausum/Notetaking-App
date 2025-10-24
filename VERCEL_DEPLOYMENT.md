# 🚀 Deploy Notetaking App to Vercel

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Vercel account (sign up at https://vercel.com)
- ✅ Supabase database already set up with `notes` table
- ✅ Code pushed to GitHub repository

---

## 🎯 Quick Deployment Steps

### Step 1: Push Code to GitHub

Make sure your latest code is on GitHub:

```bash
git add .
git commit -m "Prepare for Vercel deployment with Supabase"
git push origin main
```

### Step 2: Import Project to Vercel

1. 去 https://vercel.com 登入
2. 撳 **"Add New..."** → **"Project"**
3. 搵你嘅 GitHub repo: `yausum/Notetaking-App`
4. 撳 **"Import"**

### Step 3: Configure Environment Variables

響 Vercel project settings，add 呢啲 environment variables:

| Key | Value | 位置 |
|-----|-------|------|
| `GITHUB_TOKEN` | `github_pat_11AH4D3LA0ylsZxF6KpQJ7_...` | 你嘅 .env |
| `OPENAI_MODEL` | `openai/gpt-4.1-mini` | 你嘅 .env |
| `SUPABASE_URL` | `https://cxffdkxgumuuukxehsib.supabase.co` | 你嘅 .env |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | 你嘅 .env |

**點樣加 Environment Variables:**
1. 響 Vercel project page，去 **Settings**
2. 撳左邊 **Environment Variables**
3. 逐個 add:
   - Name: `GITHUB_TOKEN`
   - Value: paste 你嘅 token
   - Environment: 揀晒 `Production`, `Preview`, `Development`
   - 撳 **"Save"**
4. 重覆 4 次，加晒上面 4 個 variables

### Step 4: Deploy!

1. 響 Vercel dashboard，撳 **"Deploy"**
2. 等 1-2 分鐘 build
3. ✅ 完成！會有個 URL 俾你（例如: `https://notetaking-app.vercel.app`）

---

## 📁 Files Created for Vercel

我已經幫你 create 咗呢啲 files:

### 1. `vercel.json` ✅
配置 Vercel build settings，指定 Python runtime 同 routes。

### 2. Updated `run.py` ✅
改咗做 compatible with Vercel serverless functions。

---

## 🔧 Vercel Configuration Details

### `vercel.json` 解釋:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "run.py",           // Entry point
      "use": "@vercel/python"     // Use Python runtime
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",      // Static files (CSS, JS)
      "dest": "/frontend/static/$1"
    },
    {
      "src": "/(.*)",             // All other routes
      "dest": "run.py"            // Go to Flask app
    }
  ]
}
```

---

## ⚠️ Important Notes

### 1. Database Table 要預先 Create

Vercel 係 serverless，每次 request 都係新 instance，所以**唔好響 app 入面 create table**。

確保你已經響 Supabase SQL Editor run 咗呢個 script:

```sql
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    tags TEXT,
    event_date DATE,
    event_time TIME,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notes_updated_at ON notes(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_notes_event_date ON notes(event_date DESC);
CREATE INDEX IF NOT EXISTS idx_notes_created_at ON notes(created_at DESC);

ALTER TABLE notes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all operations for notes" ON notes;
CREATE POLICY "Allow all operations for notes" 
ON notes FOR ALL 
USING (true) 
WITH CHECK (true);
```

### 2. Environment Variables

**絕對唔好 commit `.env` file 去 GitHub！**

確保 `.gitignore` 有呢行:
```
.env
```

所有 secrets 要響 Vercel Dashboard 入面 set。

### 3. Cold Start

Serverless functions 有 "cold start" time（第一次 request 會慢啲）。之後就會快。

### 4. Logs

Check logs 響 Vercel Dashboard → **Deployments** → 揀個 deployment → **"View Function Logs"**

---

## 🐛 Troubleshooting

### Error: "Module not found"

**Solution**: 確保 `requirements.txt` 有晒所有 dependencies:
```
Flask==3.0.0
Werkzeug==3.0.1
python-dotenv==1.0.0
openai==1.106.1
supabase==2.10.0
```

### Error: "Database connection failed"

**Solution**: 
1. Check Vercel environment variables 有冇 set 錯
2. 去 Supabase → Project Settings → API，confirm URL 同 key
3. Make sure Supabase project 冇 pause（free tier 會 auto-pause after 7 days inactivity）

### Error: "Build failed"

**Solution**: Check Vercel build logs，通常係 Python version 或 dependency 問題。

Vercel 預設用 Python 3.9。如果需要指定 version，响 `runtime.txt` add:
```
python-3.11
```

### Static Files 404

**Solution**: 確保 `vercel.json` routes 設定正確，同埋 static files 响 `frontend/static/` folder。

---

## 📊 After Deployment

### Custom Domain (Optional)

1. 響 Vercel project → **Settings** → **Domains**
2. Add 你自己嘅 domain (如果有)
3. Update DNS records as instructed

### Monitoring

- **Analytics**: Vercel Dashboard → **Analytics**
- **Logs**: Vercel Dashboard → **Deployments** → **Function Logs**
- **Performance**: Check Response Times 响 Analytics

---

## 🔄 Update 你嘅 App

之後如果要 update code:

1. Make changes locally
2. Test locally: `python run.py`
3. Commit & push:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
4. Vercel 會 **automatically redeploy**！ 🚀

---

## 🎉 Done!

Your app should be live at: `https://your-project-name.vercel.app`

你可以 share 呢個 URL 俾人用！ 🌐

---

## 💡 Pro Tips

1. **Preview Deployments**: 每個 branch 都有自己嘅 preview URL for testing
2. **Rollback**: 可以 instant rollback 去之前嘅 deployment
3. **Edge Network**: Vercel 用 global CDN，全世界都快
4. **Free Tier**: 足夠 personal projects（100GB bandwidth/month）

---

**有問題？Check Vercel docs**: https://vercel.com/docs

Good luck! 🚀
