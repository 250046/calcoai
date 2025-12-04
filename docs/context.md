# 🧠 Project: Calco AI – Telegram Personal Finance Assistant Bot

## 🎯 GOAL
Build a Telegram bot called **Calco AI** that helps users manage their personal finances through text and voice. The bot should understand user messages like "I spent 15,000 on groceries" and automatically log them into a PostgreSQL database. It will also support income logging, debt tracking, and reminders.

## 📱 FEATURES

### 1. Voice & Text Recognition
- Accept audio or text input from users.
- Transcribe audio using OpenAI Whisper API.
- Parse input to extract:
  - `amount`
  - `type` (income, expense)
  - `category`
  - `description`
  - `date`

### 2. Finance Tracking
- Log expenses and incomes.
- Save transaction data to PostgreSQL (Supabase).
- Fetch summaries and daily/monthly reports.

### 3. Loan Tracking
- Allow users to record loans given to others.
- Include fields: `amount`, `person`, `due_date`, `status`.
- Schedule reminder messages.

### 4. User Onboarding
- Ask for language selection on first launch (Uzbek / Russian).
- Save basic user info in the database.

### 5. Monetization (future)
- Subscription tiers can be managed in DB.
- Restrict premium features to paid users.

---

## 🛠 TECH STACK

### 🧩 BOT ENGINE
- **Library:** `Pyrogram`
- **Platform:** Telegram Bot API

### 🔊 AUDIO TRANSCRIPTION
- **Service:** OpenAI Whisper API

### 🧠 NLP / DATA EXTRACTION
- **Service:** OpenAI GPT-3.5 or GPT-4
- **Goal:** Extract structured data from natural speech or text (e.g. amount, category, type)

### ⚙️ BACKEND
- **Framework:** FastAPI
- **Purpose:** Handle API endpoints (optional), internal logic

### 🗃 DATABASE
- **Type:** PostgreSQL
- **Provider:** Supabase
- **Tables:**
  - `users`
  - `transactions`
  - `loans`
  - `subscriptions` (for later)

### ☁️ DEPLOYMENT
- **Platform:** Railway.app
- **Bot runs as a daemon process (no sleeping)**
- `.env` file for secrets

---

## 🧱 DATABASE SCHEMA (Supabase)

### Table: `users`
| Column       | Type      |
|--------------|-----------|
| id           | bigint (PK) |
| telegram_id  | bigint UNIQUE |
| name         | text |
| created_at   | timestamp (default now()) |

---

### Table: `transactions`
| Column      | Type      |
|-------------|-----------|
| id          | bigint (PK) |
| user_id     | bigint (FK to users.id) |
| amount      | numeric |
| type        | text ('income' or 'expense') |
| category    | text |
| description | text |
| date        | date (default current_date) |

---

### Table: `loans`
| Column       | Type     |
|--------------|----------|
| id           | bigint (PK) |
| user_id      | bigint (FK to users.id) |
| person_name  | text |
| amount       | numeric |
| given_date   | date |
| return_date  | date |
| status       | text ('pending', 'paid') |

---

## 🔐 ENVIRONMENT VARIABLES (.env)

```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:pass@host:port/dbname
