import openai
from config import OPENAI_API_KEY
import json
from typing import Dict, Optional
from datetime import datetime
import os
from currency_converter import currency_converter

openai.api_key = OPENAI_API_KEY

class AIParser:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Initialize Yandex SpeechKit if credentials are available
        self.yandex_speech = None
        yandex_api_key = os.getenv("YANDEX_API_KEY")
        yandex_folder_id = os.getenv("YANDEX_FOLDER_ID")
        
        if yandex_api_key and yandex_folder_id:
            from yandex_speech import YandexSpeechKit
            self.yandex_speech = YandexSpeechKit(yandex_api_key, yandex_folder_id)
            print("✅ Yandex SpeechKit initialized for Uzbek")
        else:
            print("⚠️  Yandex credentials not found - using Whisper for all languages")
    
    def transcribe_audio(self, audio_file_path: str, language: str = "uz") -> str:
        """
        Transcribe audio using best service for the language
        - Uzbek: Yandex SpeechKit (if available)
        - Russian/English: OpenAI Whisper
        """
        
        # Use Yandex for Uzbek if available
        if language == "uz" and self.yandex_speech:
            print("🎤 Using Yandex SpeechKit for Uzbek...")
            text = self.yandex_speech.transcribe_with_fallback(audio_file_path, "uz-UZ")
            if text:
                return text
            else:
                print("⚠️  Yandex failed, falling back to Whisper...")
        
        # Use Whisper for Russian, English, or as fallback
        print("🎤 Using OpenAI Whisper...")
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        return transcript.text

    
    def parse_transaction(self, text: str, language: str = "uz", user_currency: str = "UZS") -> Optional[Dict]:
        """Extract transaction data from text using GPT - handles single or multiple transactions"""
        prompt = f"""
You are a financial assistant. Extract transaction information from the user's message.

IMPORTANT: The user might mention MULTIPLE transactions in one message.

If there is ONE transaction, return a JSON object:
{{"amount": number, "type": "income/expense", "category": string, "description": string, "date": "YYYY-MM-DD", "currency": "USD/EUR/UZS/etc"}}

If there are MULTIPLE transactions, return a JSON array:
[
  {{"amount": number, "type": "income/expense", "category": string, "description": string, "date": "YYYY-MM-DD", "currency": "USD/EUR/UZS/etc"}},
  {{"amount": number, "type": "income/expense", "category": string, "description": string, "date": "YYYY-MM-DD", "currency": "USD/EUR/UZS/etc"}}
]

IMPORTANT: Extract the currency from the text (USD, EUR, $, €, etc.). If no currency mentioned, use "UZS".

User message: "{text}"
Language: {language}

Common categories:
Expense: food, transport, housing, health, entertainment, shopping, education, other
Income: salary, business, gift, investment, other

Examples:
- "5000 for coffee" → single transaction
- "5000 for coffee, 10000 for hotdog, 20000 for kebab" → array of 3 transactions
- "I bought coffee for 5000 then hotdog for 10000" → array of 2 transactions

If you cannot extract valid transaction data, return: {{"error": "Cannot parse transaction"}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial data extraction assistant. Always respond with valid JSON only. Return an array if multiple transactions are mentioned."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            result = json.loads(result_text)
            
            # Check if error
            if isinstance(result, dict) and "error" in result:
                return None
            
            # Handle both single transaction (dict) and multiple transactions (list)
            if isinstance(result, list):
                # Multiple transactions - return as special format
                transactions = []
                for trans in result:
                    if "amount" in trans and "type" in trans:
                        # Set defaults for each transaction
                        if "category" not in trans:
                            trans["category"] = "other"
                        if "description" not in trans:
                            trans["description"] = text[:100]
                        if "date" not in trans:
                            trans["date"] = datetime.now().strftime("%Y-%m-%d")
                        
                        # Currency conversion
                        trans_currency = trans.get("currency", "UZS")
                        if trans_currency != user_currency:
                            original_amount = trans["amount"]
                            trans["amount"] = currency_converter.convert(
                                original_amount, trans_currency, user_currency
                            )
                            trans["original_amount"] = original_amount
                            trans["original_currency"] = trans_currency
                        trans["currency"] = user_currency
                        
                        transactions.append(trans)
                
                if transactions:
                    return {"multiple": True, "transactions": transactions}
                else:
                    return None
            
            # Single transaction
            if "amount" not in result or "type" not in result:
                return None
            
            # Set defaults
            if "category" not in result:
                result["category"] = "other"
            if "description" not in result:
                result["description"] = text[:100]
            if "date" not in result:
                result["date"] = datetime.now().strftime("%Y-%m-%d")
            
            # Currency conversion
            trans_currency = result.get("currency", "UZS")
            if trans_currency != user_currency:
                original_amount = result["amount"]
                result["amount"] = currency_converter.convert(
                    original_amount, trans_currency, user_currency
                )
                result["original_amount"] = original_amount
                result["original_currency"] = trans_currency
            result["currency"] = user_currency
            
            return result
        except Exception as e:
            print(f"AI parsing error: {e}")
            return None

ai_parser = AIParser()
