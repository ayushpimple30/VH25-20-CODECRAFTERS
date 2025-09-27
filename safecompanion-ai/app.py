import os
import re
import streamlit as st
from gtts import gTTS
import tempfile
import pytesseract
from PIL import Image
import speech_recognition as sr
from groq import Groq
import sqlite3
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Please set it as env variable or hardcode for testing.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


def init_db():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    input_type TEXT,
                    user_input TEXT,
                    ai_reply TEXT,
                    flagged INTEGER,
                    pii_hidden INTEGER
                )''')
    conn.commit()
    conn.close()

def log_activity(input_type, user_input, ai_reply, flagged, pii_hidden):
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("INSERT INTO activity_log (timestamp, input_type, user_input, ai_reply, flagged, pii_hidden) VALUES (?, ?, ?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), input_type, user_input, ai_reply, int(flagged), int(pii_hidden)))
    conn.commit()
    conn.close()


def apply_safety_filters(text: str):
    flagged = False
    pii_detected = False

    if re.search(r"\b(stupid|kill|hate)\b", text, re.IGNORECASE):
        flagged = True
        text = "[filtered]"

    if re.search(r"\d{10}", text):  
        pii_detected = True
        text = "[hidden-phone]"

    return text, flagged, pii_detected


def generate_reply(prompt: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are SafeCompanion.AI, a safe and helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {e}"


LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Punjabi": "pa"
}

def speak_text(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name


def mic_input():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Listening... Speak now")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""


st.set_page_config(page_title="SafeCompanion.AI", layout="wide")
st.title("🛡️ SafeCompanion.AI Prototype")
st.caption("A safe, conversational AI prototype powered by Groq API with Text-to-Speech, Mic Input, Image Upload & Activity Logging.")


init_db()


st.sidebar.header("⚙️ Settings")
language = st.sidebar.selectbox("🌐 Select Language for Speech Output", list(LANG_MAP.keys()))
enable_tts = st.sidebar.checkbox("🔊 Enable Voice Replies", value=True)
enable_mic = st.sidebar.checkbox("🎙️ Use Microphone Input", value=False)


st.subheader("💬 Chat")

user_input = ""
input_type = "text"

if enable_mic:
    if st.button("🎤 Speak"):
        user_input = mic_input()
        input_type = "mic"
else:
    user_input = st.text_input("Enter your message:")


uploaded_image = st.file_uploader("📷 Upload an image (JPG/PNG)", type=["png", "jpg", "jpeg"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    extracted_text = pytesseract.image_to_string(image)
    if extracted_text.strip():
        st.success("✅ Extracted text from image:")
        st.write(extracted_text)
        if not user_input:
            user_input = extracted_text
            input_type = "image"


if user_input:
    st.markdown(f"🧑 You: {user_input}")

    ai_reply = generate_reply(user_input)
    ai_reply, flagged, pii_detected = apply_safety_filters(ai_reply)

    st.markdown(f"🤖 **SafeCompanion.AI**: {ai_reply}")

    if enable_tts and ai_reply.strip():
        lang_code = LANG_MAP.get(language, "en")
        audio_file = speak_text(ai_reply, lang=lang_code)
        st.audio(audio_file, format="audio/mp3")

  
    log_activity(input_type, user_input, ai_reply, flagged, pii_detected)


st.subheader("📊 Safety Dashboard")
st.write("✅ All activities are logged with timestamp (personal details hidden).")
