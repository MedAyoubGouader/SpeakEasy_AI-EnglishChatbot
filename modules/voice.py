"""
🎤 VOICE MODULE
Speech-to-Text (STT) and Text-to-Speech (TTS) functionality
"""

import tempfile
import os
from gtts import gTTS
import base64

class VoiceAssistant:
    """Handle all voice-related functionality"""
    
    def __init__(self, accent="en"):
        """
        Initialize voice assistant
        accent: 'en' (US), 'en-gb' (UK), 'en-au' (Australian)
        """
        self.accent = accent
        self.tld_map = {
            "US": "com",
            "UK": "co.uk",
            "Australian": "com.au"
        }
    
    def text_to_speech(self, text: str, accent: str = "US") -> str:
        """
        Convert text to speech and return audio file path
        
        Args:
            text: The text to convert to speech
            accent: Voice accent (US, UK, Australian)
            
        Returns:
            Path to the generated audio file
        """
        try:
            tld = self.tld_map.get(accent, "com")
            tts = gTTS(text=text, lang='en', tld=tld, slow=False)
            
            # Create temp file
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(audio_file.name)
            
            return audio_file.name
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def get_audio_player(self, audio_path: str) -> str:
        """
        Generate HTML audio player for autoplay
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            HTML string for audio player
        """
        try:
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'''
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            '''
            return audio_html
        except Exception as e:
            print(f"Audio player error: {e}")
            return ""
    
    def speak(self, text: str, accent: str = "US"):
        """
        Convert text to speech and return audio path
        
        Args:
            text: Text to speak
            accent: Voice accent
            
        Returns:
            Audio file path or None
        """
        # Limit text length to avoid long audio
        if len(text) > 500:
            text = text[:500] + "..."
        
        return self.text_to_speech(text, accent)


class SpeechRecognizer:
    """Handle speech recognition (placeholder for future implementation)"""
    
    def __init__(self):
        self.is_listening = False
    
    def start_listening(self):
        """Start listening for speech"""
        self.is_listening = True
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
    
    def recognize(self, audio_data) -> str:
        """
        Recognize speech from audio data
        
        Args:
            audio_data: Audio bytes
            
        Returns:
            Recognized text
        """
        # Placeholder - would use Whisper or SpeechRecognition
        return ""


# Utility functions
def cleanup_audio(file_path: str):
    """Remove temporary audio file"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except:
        pass
