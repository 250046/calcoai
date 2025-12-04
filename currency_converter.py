"""
Currency converter for Calco AI
Uses exchange rates to convert between currencies
"""
import requests
from typing import Optional

# Exchange rates (UZS as base)
# Update these periodically or use an API
EXCHANGE_RATES = {
    "UZS": 1,
    "USD": 12700,  # 1 USD = 12700 UZS
    "EUR": 13800,  # 1 EUR = 13800 UZS
    "RUB": 130,    # 1 RUB = 130 UZS
    "KZT": 26,     # 1 KZT = 26 UZS
}

class CurrencyConverter:
    def __init__(self):
        self.rates = EXCHANGE_RATES
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert amount from one currency to another
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code (USD, EUR, UZS, etc.)
            to_currency: Target currency code
        
        Returns:
            Converted amount
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # If same currency, no conversion needed
        if from_currency == to_currency:
            return amount
        
        # Convert to UZS first, then to target currency
        if from_currency not in self.rates or to_currency not in self.rates:
            # Unknown currency, return original amount
            return amount
        
        # Convert from source to UZS
        amount_in_uzs = amount * self.rates[from_currency]
        
        # Convert from UZS to target
        result = amount_in_uzs / self.rates[to_currency]
        
        return round(result, 2)
    
    def detect_currency(self, text: str) -> Optional[str]:
        """
        Detect currency mentioned in text
        Returns currency code or None
        """
        text_upper = text.upper()
        
        # Check for currency symbols and codes
        currency_patterns = {
            "$": "USD",
            "USD": "USD",
            "DOLLAR": "USD",
            "€": "EUR",
            "EUR": "EUR",
            "EURO": "EUR",
            "₽": "RUB",
            "RUB": "RUB",
            "RUBLE": "RUB",
            "₸": "KZT",
            "KZT": "KZT",
            "TENGE": "KZT",
            "SOM": "UZS",
            "SO'M": "UZS",
            "UZS": "UZS",
        }
        
        for pattern, currency in currency_patterns.items():
            if pattern in text_upper:
                return currency
        
        return None

currency_converter = CurrencyConverter()
