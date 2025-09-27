import streamlit as st
from transformers import pipeline
from gtts import gTTS
import re
import os
import base64

# Load model
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

model = load_model()

# Safety filter function
def apply_safety_filters(user_input):
    # Block harmful words
    bad_words = ["stupid", "idiot", "fuck", "shit"]
    for word in bad_words:
        if word in user_input.lower():
            return "[filtered]"

    # Hide phone numbers
    user_input = re.sub(r"\b\d{10,}\b", "[hidden-phone]", user_input)

    # Hide emails
    user_input = re.sub(r"\S+@\S+\.\S+", "[hidden-email]", user_input)

    return user_input

# Math detection
def check_math(user_input):
    try:
        if re.match(r"^[0-9+\-*/(). ]+$", user_input):
            return str(eval(user_input))
    except:
        return None
    return None

# Generate AI reply
def generate_reply(user_input):
    # First check filters
    clean_input = apply_safety_filters(user_input)

    if clean_input != user_input:
        return clean_input

    # Check math
    math_result = check_math(user_input)
    if math_result is not None:
        return math_result

    # Normal AI response
    response = model(clean_input, max_length=100, do_sample=True)[0]['generated_text']
    return response

# Text to Speech function
def text_to_speech(text, filename="tts_output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    return f'<audio autoplay controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# Streamlit UI
st.title("🛡️ SafeCompanion.AI Prototype")
st.write("A safe, conversational AI prototype with Text-to-Speech")

# TTS toggle
enable_tts = st.checkbox("Enable Voice")

# Chat
st.subheader("💬 Chat")
user_input = st.text_input("Enter your message:")

if user_input:
    st.markdown(f"👤 You: {user_input}")
    ai_reply = generate_reply(user_input)
    st.markdown(f"🤖 SafeCompanion.AI: {ai_reply}")

    # Voice playback if enabled
    if enable_tts and ai_reply not in ["[filtered]", "[hidden-phone]", "[hidden-email]"]:
        st.markdown(text_to_speech(ai_reply), unsafe_allow_html=True)

# Safety Dashboard
st.subheader("📊 Safety Dashboard")
st.write("✅ Harmful words or private info are automatically filtered.")
