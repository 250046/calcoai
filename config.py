import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Language settings
LANGUAGES = {
    "uz": "🇺🇿 O'zbek",
    "ru": "🇷🇺 Русский"
}

# Categories
EXPENSE_CATEGORIES = {
    "uz": ["🍔 Oziq-ovqat", "🚗 Transport", "🏠 Uy-joy", "💊 Sog'liq", "🎮 O'yin-kulgi", "🛒 Xarid", "📚 Ta'lim", "💰 Boshqa"],
    "ru": ["🍔 Еда", "🚗 Транспорт", "🏠 Жилье", "💊 Здоровье", "🎮 Развлечения", "🛒 Покупки", "📚 Образование", "💰 Другое"]
}

INCOME_CATEGORIES = {
    "uz": ["💼 Ish haqi", "💰 Biznes", "🎁 Sovg'a", "📈 Investitsiya", "💵 Boshqa"],
    "ru": ["💼 Зарплата", "💰 Бизнес", "🎁 Подарок", "📈 Инвестиции", "💵 Другое"]
}
