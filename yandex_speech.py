"""
Yandex SpeechKit integration for Uzbek speech recognition
"""
import requests
import json
from typing import Optional

class YandexSpeechKit:
    def __init__(self, api_key: str, folder_id: str):
        """
        Initialize Yandex SpeechKit
        
        Args:
            api_key: Yandex Cloud API key
            folder_id: Yandex Cloud folder ID
        """
        self.api_key = api_key
        self.folder_id = folder_id
        self.api_url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
    
    def transcribe_audio(self, audio_file_path: str, language: str = "uz-UZ") -> Optional[str]:
        """
        Transcribe audio file using Yandex SpeechKit
        
        Args:
            audio_file_path: Path to audio file (OGG, MP3, WAV)
            language: Language code (uz-UZ for Uzbek, ru-RU for Russian)
        
        Returns:
            Transcribed text or None if failed
        """
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Prepare request
            headers = {
                'Authorization': f'Api-Key {self.api_key}',
            }
            
            params = {
                'lang': language,
                'folderId': self.folder_id,
                'format': 'oggopus',  # Telegram voice messages are OGG Opus
            }
            
            # Send request
            response = requests.post(
                self.api_url,
                headers=headers,
                params=params,
                data=audio_data,
                timeout=30
            )
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    text = result['result']
                    print(f"Yandex transcription: {text}")
                    return text
                else:
                    print(f"Yandex response has no result: {result}")
                    return None
            else:
                print(f"Yandex API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Yandex transcription error: {e}")
            return None
    
    def transcribe_with_fallback(self, audio_file_path: str, language: str = "uz-UZ") -> Optional[str]:
        """
        Transcribe with automatic fallback to Russian if Uzbek fails
        """
        # Try primary language
        text = self.transcribe_audio(audio_file_path, language)
        
        # If failed and language is Uzbek, try Russian (common code-switching)
        if not text and language == "uz-UZ":
            print("Uzbek transcription failed, trying Russian...")
            text = self.transcribe_audio(audio_file_path, "ru-RU")
        
        return text
