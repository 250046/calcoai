# 🤖 Calco AI - Telegram Personal Finance Bot

A smart Telegram bot that helps users manage their personal finances through text and voice messages.

## ✨ Features

- 🎤 **Voice & Text Recognition** - Send expenses via voice or text
- 💰 **Finance Tracking** - Automatic expense and income logging
- 📊 **Reports** - Daily and monthly financial summaries
- 💸 **Loan Management** - Track money lent to others
- 🌐 **Multi-language** - Uzbek and Russian support
- 🤖 **AI-Powered** - Uses OpenAI GPT for natural language understanding

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Run the SQL from `schema.sql` in the SQL Editor
4. Copy your credentials to `.env`

### 3. Configure Environment

The `.env` file is already configured with your credentials.

### 4. Run the Bot

```bash
python bot.py
```

## 📁 Project Structure

```
calco-ai/
├── bot.py              # Main bot logic
├── database.py         # Database operations
├── ai_parser.py        # AI transcription & parsing
├── translations.py     # Multi-language support
├── config.py           # Configuration
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

## 💬 Usage Examples

**Text:**
- "I spent 15,000 on groceries"
- "Received salary 5,000,000"
- "25,000 for transport today"

**Voice:**
- Just send a voice message describing your transaction

**Loans:**
- "Lent Ali 100,000"
- "Gave 50,000 to friend"

## 🔧 Configuration

Edit `.env` to update:
- `BOT_TOKEN` - Your Telegram bot token
- `OPENAI_API_KEY` - OpenAI API key
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase service role key

## 🚀 Deployment to Railway

1. Create account on [Railway.app](https://railway.app)
2. Create new project
3. Connect your GitHub repo
4. Add environment variables from `.env`
5. Deploy!

## 📝 Commands

- `/start` - Start the bot and show main menu

## 🛠 Tech Stack

- **Bot Framework:** Pyrogram
- **AI:** OpenAI GPT-3.5 & Whisper
- **Database:** PostgreSQL (Supabase)
- **Language:** Python 3.9+

## 📄 License

MIT License - feel free to use and modify!
