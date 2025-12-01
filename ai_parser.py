import openai
from config import OPENAI_API_KEY
import json
from typing import Dict, Optional
from datetime import datetime

openai.api_key = OPENAI_API_KEY

class AIParser:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def transcribe_audio(self, audio_file_path: str, language: str = "uz") -> str:
        """Transcribe audio using Whisper API"""
        with open(audio_file_path, "rb") as audio_file:
            # Whisper doesn't support 'uz' (Uzbek), so we don't specify language
            # Let Whisper auto-detect the language (it supports 99+ languages)
            # For Russian, we can specify 'ru', but for Uzbek we let it auto-detect
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
                # No language parameter - auto-detect works better
            )
        return transcript.text
    
    def parse_transaction(self, text: str, language: str = "uz") -> Optional[Dict]:
        """Extract transaction data from text using GPT"""
        prompt = f"""
You are a financial assistant. Extract transaction information from the user's message.
Return ONLY a valid JSON object with these fields:
- amount (number, required)
- type ("income" or "expense", required)
- category (string, required)
- description (string, optional)
- date (YYYY-MM-DD format, default to today if not mentioned)

User message: "{text}"
Language: {language}

Common categories:
Expense: food, transport, housing, health, entertainment, shopping, education, other
Income: salary, business, gift, investment, other

If you cannot extract valid transaction data, return: {{"error": "Cannot parse transaction"}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial data extraction assistant. Always respond with valid JSON only."},
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
            
            if "error" in result:
                return None
            
            # Validate required fields
            if "amount" not in result or "type" not in result:
                return None
            
            # Set defaults
            if "category" not in result:
                result["category"] = "other"
            if "description" not in result:
                result["description"] = text[:100]
            if "date" not in result:
                result["date"] = datetime.now().strftime("%Y-%m-%d")
            
            return result
        except Exception as e:
            print(f"AI parsing error: {e}")
            return None

ai_parser = AIParser()
