# ⚡ Quick Start - Calco AI

## 🏃 Get Running in 5 Minutes

### 1️⃣ Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Database (2 min)
1. Open [Supabase SQL Editor](https://supabase.com/dashboard/project/aziunnsepxxavwrvafpv/sql)
2. Copy contents of `schema.sql`
3. Paste and click **Run**

### 3️⃣ Test Setup (1 min)
```bash
python test_bot.py
```

### 4️⃣ Run Bot (1 min)
```bash
python bot.py
```

### 5️⃣ Test on Telegram
Send `/start` to your bot!

---

## 📱 User Commands

| Command | Description |
|---------|-------------|
| `/start` | Start bot & show menu |

## 💬 Example Messages

### Expenses
- "I spent 15000 on groceries"
- "Paid 50000 for rent"
- "25000 for transport today"

### Income
- "Received salary 5000000"
- "Got 100000 from freelance"
- "Earned 200000 today"

### Loans
- "Lent Ali 100000"
- "Gave 50000 to friend"

---

## 🚀 Deploy to Railway (5 min)

### Quick Deploy
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Set variabless)
railway variables set BOT_TOKEN=your_bot_token
railway variables set API_ID=your_api_id
railway variables set API_HASH=your_api_hash
railway variables set OPENAI_API_KEY=your_openai_key
url
railway se_keyur_supabaASE_KEY=yoPABables set SUvariase_supabURL=your_t SUPABASE_ seiablesarway vilra

# Deploy
railway up
```

---

## 🐛 Quick Troubleshooting

### Bot not responding?
```bash
# Check if running
ps aux | grep bot.py

# Restart
python bot.py
```

### Database error?
```bash
# Test connection
python test_bot.py
```

### AI not working?
- Check OpenAI credits
- Verify API key is valid
- Test with simple message

---

## 📊 Project Files

| File | Purpose |
|------|---------|
| `bot.py` | Main bot code |
| `database.py` | Database operations |
| `ai_parser.py` | AI parsing |
| `schema.sql` | Database schema |
| `.env` | Your credentials |

---

## 🎯 Next Steps

1. ✅ Get bot running locally
2. ✅ Test all features
3. ✅ Deploy to Railway
4. 📱 Share bot with users
5. 📊 Monitor usage
6. 🚀 Add premium features

---

## 💡 Tips

- Use voice messages for faster input
- Check monthly reports regularly
- Track loans to remember debts
- Switch language in settings
- Bot works in private chats only

---

## 🆘 Need Help?

1. Read `SETUP_GUIDE.md` for detailed instructions
2. Check `README.md` for full documentation
3. Run `python test_bot.py` to diagnose issues
4. Check Railway logs if deployed

---

**🎉 You're all set! Start tracking your finances with Calco AI!**
