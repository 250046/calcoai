"""
Utility functions for Calco AI bot
"""
from datetime import datetime, timedelta
from typing import Dict, List

def format_currency(amount: float) -> str:
    """Format amount with thousand separators"""
    return f"{amount:,.0f}".replace(",", " ")

def format_date(date_str: str) -> str:
    """Format date to readable format"""
    try:
        date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except:
        return str(date_str)

def get_month_name(month: int, lang: str = "uz") -> str:
    """Get month name in specified language"""
    months_uz = [
        "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
        "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
    ]
    months_ru = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    
    months = months_uz if lang == "uz" else months_ru
    return months[month - 1] if 1 <= month <= 12 else str(month)

def calculate_category_breakdown(transactions: List[Dict]) -> Dict[str, float]:
    """Calculate spending by category"""
    breakdown = {}
    for trans in transactions:
        category = trans.get("category", "other")
        amount = trans.get("amount", 0)
        breakdown[category] = breakdown.get(category, 0) + amount
    return breakdown

def get_date_range(period: str = "month") -> tuple:
    """Get start and end dates for a period"""
    today = datetime.now()
    
    if period == "today":
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today
    elif period == "week":
        start = today - timedelta(days=today.weekday())
        end = today
    elif period == "month":
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = today
    elif period == "year":
        start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = today
    else:
        start = today
        end = today
    
    return start.date(), end.date()

def validate_amount(text: str) -> float:
    """Extract and validate amount from text"""
    import re
    # Remove spaces and find numbers
    numbers = re.findall(r'\d+', text.replace(" ", ""))
    if numbers:
        return float(numbers[0])
    return 0.0

def generate_transaction_emoji(trans_type: str, category: str) -> str:
    """Get emoji for transaction type and category"""
    if trans_type == "income":
        return "💰"
    
    # Expense emojis by category
    category_emojis = {
        "food": "🍔",
        "transport": "🚗",
        "housing": "🏠",
        "health": "💊",
        "entertainment": "🎮",
        "shopping": "🛒",
        "education": "📚",
        "other": "💸"
    }
    
    return category_emojis.get(category.lower(), "💸")

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def is_valid_telegram_id(telegram_id: int) -> bool:
    """Validate Telegram user ID"""
    return isinstance(telegram_id, int) and telegram_id > 0

def parse_loan_info(text: str) -> Dict:
    """Parse loan information from text"""
    import re
    
    # Extract amount
    amounts = re.findall(r'\d+', text.replace(" ", ""))
    amount = float(amounts[0]) if amounts else 0
    
    # Extract person name (first word that's not a number)
    words = text.split()
    person = "Unknown"
    for word in words:
        if not word.isdigit() and len(word) > 2:
            person = word.capitalize()
            break
    
    return {
        "amount": amount,
        "person": person
    }
