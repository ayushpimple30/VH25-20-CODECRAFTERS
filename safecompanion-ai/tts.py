from gtts import gTTS
import tempfile
import os

def speak_text(text: str, lang: str = "en"):
    """
    Convert text to speech and return the audio file path.
    Default language is English (en), but can be switched 
    e.g. Hindi (hi), Marathi (mr), Tamil (ta), Telugu (te), Gujarati (gu), Punjabi (pa).
    """
    if not text.strip():
        return None

    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        print(f"[TTS Error] {e}")
        return None
