from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BOT_TOKEN, API_ID, API_HASH
from database import db
from ai_parser import ai_parser
from translations import t, TRANSLATIONS
import os
from datetime import datetime

# User states
user_states = {}

# Initialize bot
app = Client(
    "calco_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def get_language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ])

def get_main_menu_keyboard(lang: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("add_expense", lang), callback_data="add_expense"),
            InlineKeyboardButton(t("add_income", lang), callback_data="add_income")
        ],
        [
            InlineKeyboardButton(t("view_history", lang), callback_data="view_history"),
            InlineKeyboardButton(t("monthly_report", lang), callback_data="monthly_report")
        ],
        [
            InlineKeyboardButton(t("manage_loans", lang), callback_data="manage_loans"),
            InlineKeyboardButton(t("settings", lang), callback_data="settings")
        ]
    ])

def get_loan_menu_keyboard(lang: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("add_loan", lang), callback_data="add_loan"),
            InlineKeyboardButton(t("view_loans", lang), callback_data="view_loans")
        ],
        [InlineKeyboardButton(t("back", lang), callback_data="main_menu")]
    ])

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user = db.get_user(message.from_user.id)
    
    if not user:
        await message.reply(
            TRANSLATIONS["uz"]["welcome"],
            reply_markup=get_language_keyboard()
        )
    else:
        lang = user.get("language", "uz")
        await message.reply(
            t("main_menu", lang),
            reply_markup=get_main_menu_keyboard(lang)
        )

@app.on_callback_query(filters.regex("^lang_"))
async def language_callback(client: Client, callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user = db.get_user(callback.from_user.id)
    
    if not user:
        db.create_user(
            telegram_id=callback.from_user.id,
            name=callback.from_user.first_name or "User",
            language=lang
        )
    else:
        db.update_user_language(callback.from_user.id, lang)
    
    await callback.message.edit_text(
        t("language_selected", lang) + "\n\n" + t("main_menu", lang),
        reply_markup=get_main_menu_keyboard(lang)
    )

@app.on_callback_query(filters.regex("^main_menu$"))
async def main_menu_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    await callback.message.edit_text(
        t("main_menu", lang),
        reply_markup=get_main_menu_keyboard(lang)
    )

@app.on_callback_query(filters.regex("^add_expense$|^add_income$"))
async def add_transaction_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    trans_type = "expense" if "expense" in callback.data else "income"
    user_states[callback.from_user.id] = {"action": f"add_{trans_type}"}
    
    await callback.message.edit_text(t("send_transaction", lang))

@app.on_callback_query(filters.regex("^view_history$"))
async def view_history_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    transactions = db.get_transactions(user["id"], limit=10)
    
    if not transactions:
        await callback.answer(t("history_empty", lang), show_alert=True)
        return
    
    text = t("history_title", lang) + "\n\n"
    for trans in transactions:
        emoji = "💰" if trans["type"] == "income" else "💸"
        text += f"{emoji} {trans['amount']} so'm - {trans['category']}\n"
        text += f"   📝 {trans['description']}\n"
        text += f"   📅 {trans['date']}\n\n"
    
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(t("back", lang), callback_data="main_menu")]
    ]))

@app.on_callback_query(filters.regex("^monthly_report$"))
async def monthly_report_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    now = datetime.now()
    summary = db.get_monthly_summary(user["id"], now.year, now.month)
    
    text = t("monthly_report_text", lang,
             month=now.month,
             income=summary["income"],
             expense=summary["expense"],
             balance=summary["balance"],
             count=len(summary["transactions"]))
    
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(t("back", lang), callback_data="main_menu")]
    ]))

@app.on_callback_query(filters.regex("^manage_loans$"))
async def manage_loans_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    await callback.message.edit_text(
        t("loan_menu", lang),
        reply_markup=get_loan_menu_keyboard(lang)
    )

@app.on_callback_query(filters.regex("^add_loan$"))
async def add_loan_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    user_states[callback.from_user.id] = {"action": "add_loan"}
    await callback.message.edit_text(t("send_loan_info", lang))

@app.on_callback_query(filters.regex("^view_loans$"))
async def view_loans_callback(client: Client, callback: CallbackQuery):
    user = db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"
    
    loans = db.get_loans(user["id"])
    
    if not loans:
        await callback.answer(t("loans_empty", lang), show_alert=True)
        return
    
    text = t("loans_list", lang)
    for loan in loans:
        status_emoji = "⏳" if loan["status"] == "pending" else "✅"
        text += t("loan_item", lang,
                  person=loan["person_name"],
                  amount=loan["amount"],
                  date=loan["given_date"],
                  status=f"{status_emoji} {loan['status']}")
    
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(t("back", lang), callback_data="manage_loans")]
    ]))

@app.on_callback_query(filters.regex("^settings$"))
async def settings_callback(client: Client, callback: CallbackQuery):
    await callback.message.edit_text(
        "⚙️ Sozlamalar / Настройки\n\nTilni o'zgartirish / Изменить язык:",
        reply_markup=get_language_keyboard()
    )

@app.on_message(filters.text & filters.private)
async def handle_text(client: Client, message: Message):
    user = db.get_user(message.from_user.id)
    
    if not user:
        await message.reply(
            TRANSLATIONS["uz"]["welcome"],
            reply_markup=get_language_keyboard()
        )
        return
    
    lang = user.get("language", "uz")
    user_id = message.from_user.id
    state = user_states.get(user_id, {})
    
    if state.get("action") == "add_loan":
        user_currency = user.get("currency", "UZS")
        result = ai_parser.parse_transaction(message.text, lang, user_currency)
        
        if result and "amount" in result:
            person_name = result.get("description", "Unknown").split()[0] if result.get("description") else "Unknown"
            
            loan = db.add_loan(
                user_id=user["id"],
                person_name=person_name,
                amount=result["amount"]
            )
            
            await message.reply(
                t("loan_added", lang,
                  person=person_name,
                  amount=result["amount"],
                  date=loan["given_date"]),
                reply_markup=get_main_menu_keyboard(lang)
            )
            user_states.pop(user_id, None)
        else:
            await message.reply(t("parse_error", lang))
    else:
        user_currency = user.get("currency", "UZS")
        result = ai_parser.parse_transaction(message.text, lang, user_currency)
        
        if result:
            # Check if multiple transactions
            if result.get("multiple"):
                # Handle multiple transactions
                transactions = result["transactions"]
                total_amount = sum(t["amount"] for t in transactions)
                
                # Save all transactions
                for trans in transactions:
                    db.add_transaction(
                        user_id=user["id"],
                        amount=trans["amount"],
                        trans_type=trans["type"],
                        category=trans["category"],
                        description=trans["description"]
                    )
                
                # Send summary message
                summary = f"✅ {len(transactions)} ta tranzaksiya qo'shildi!\n\n" if lang == "uz" else f"✅ Добавлено {len(transactions)} транзакций!\n\n"
                
                for i, trans in enumerate(transactions, 1):
                    emoji = "💰" if trans["type"] == "income" else "💸"
                    summary += f"{i}. {emoji} {trans['amount']} so'm - {trans['category']}\n"
                    summary += f"   📝 {trans['description']}\n\n"
                
                summary += f"💵 Jami: {total_amount} so'm" if lang == "uz" else f"💵 Всего: {total_amount} сум"
                
                await message.reply(summary, reply_markup=get_main_menu_keyboard(lang))
                user_states.pop(user_id, None)
            else:
                # Single transaction
                transaction = db.add_transaction(
                    user_id=user["id"],
                    amount=result["amount"],
                    trans_type=result["type"],
                    category=result["category"],
                    description=result["description"]
                )
                
                await message.reply(
                    t("transaction_added", lang,
                      amount=result["amount"],
                      category=result["category"],
                      description=result["description"],
                      date=transaction["date"]),
                    reply_markup=get_main_menu_keyboard(lang)
                )
                user_states.pop(user_id, None)
        else:
            await message.reply(t("parse_error", lang))

@app.on_message(filters.voice & filters.private)
async def handle_voice(client: Client, message: Message):
    user = db.get_user(message.from_user.id)
    
    if not user:
        await message.reply(
            TRANSLATIONS["uz"]["welcome"],
            reply_markup=get_language_keyboard()
        )
        return
    
    lang = user.get("language", "uz")
    status_msg = await message.reply(t("voice_processing", lang))
    
    try:
        voice_file = await message.download()
        text = ai_parser.transcribe_audio(voice_file, lang)
        os.remove(voice_file)
        
        # Delete processing message (don't show transcribed text to user)
        await status_msg.delete()
        
        user_currency = user.get("currency", "UZS")
        result = ai_parser.parse_transaction(text, lang, user_currency)
        
        if result:
            # Check if multiple transactions
            if result.get("multiple"):
                # Handle multiple transactions
                transactions = result["transactions"]
                total_amount = sum(t["amount"] for t in transactions)
                
                # Save all transactions
                for trans in transactions:
                    db.add_transaction(
                        user_id=user["id"],
                        amount=trans["amount"],
                        trans_type=trans["type"],
                        category=trans["category"],
                        description=trans["description"]
                    )
                
                # Send summary message
                summary = f"✅ {len(transactions)} ta tranzaksiya qo'shildi!\n\n" if lang == "uz" else f"✅ Добавлено {len(transactions)} транзакций!\n\n"
                
                for i, trans in enumerate(transactions, 1):
                    emoji = "💰" if trans["type"] == "income" else "💸"
                    summary += f"{i}. {emoji} {trans['amount']} so'm - {trans['category']}\n"
                    summary += f"   📝 {trans['description']}\n\n"
                
                summary += f"💵 Jami: {total_amount} so'm" if lang == "uz" else f"💵 Всего: {total_amount} сум"
                
                await message.reply(summary, reply_markup=get_main_menu_keyboard(lang))
            else:
                # Single transaction
                transaction = db.add_transaction(
                    user_id=user["id"],
                    amount=result["amount"],
                    trans_type=result["type"],
                    category=result["category"],
                    description=result["description"]
                )
                
                await message.reply(
                    t("transaction_added", lang,
                      amount=result["amount"],
                      category=result["category"],
                      description=result["description"],
                      date=transaction["date"]),
                    reply_markup=get_main_menu_keyboard(lang)
                )
        else:
            await message.reply(t("parse_error", lang))
    
    except Exception as e:
        print(f"Voice processing error: {e}")
        await status_msg.edit_text(t("transaction_error", lang))

if __name__ == "__main__":
    print("🤖 Calco AI Bot is starting...")
    app.run()
