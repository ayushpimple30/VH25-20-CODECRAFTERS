import os
import re
import streamlit as st
from gtts import gTTS
import tempfile
from groq import Groq

# -------------------------------
# Load API key
# -------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Please set it in .env or environment variables")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -------------------------------
# Safety Filters
# -------------------------------
harmful_words = ["stupid", "idiot", "hate", "kill", "suicide", "die"]
pii_patterns = [
    r"\b\d{10}\b",               # Phone numbers
    r"\b\d{16}\b",               # Credit card numbers
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Emails
]

def apply_safety_filters(user_input: str) -> (str, bool, bool):
    """Apply harmful word filtering and mask PII."""
    flagged = False
    pii_detected = False

    # Replace harmful words
    for word in harmful_words:
        if re.search(rf"\b{word}\b", user_input, re.IGNORECASE):
            user_input = re.sub(rf"\b{word}\b", "[filtered]", user_input, flags=re.IGNORECASE)
            flagged = True

    # Mask PII
    for pattern in pii_patterns:
        if re.search(pattern, user_input):
            user_input = re.sub(pattern, "[hidden]", user_input)
            pii_detected = True

    return user_input, flagged, pii_detected

# -------------------------------
# Groq AI Reply Generator
# -------------------------------
def generate_reply(user_input: str, model: str = "llama-3.1-8b-instant") -> str:
    """Send query to Groq API with fallback models."""
    fallback_models = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "deepseek-r1-distill-llama-70b",
        "gemma2-9b-it",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "moonshotai/kimi-k2-instruct",
        "allam-2-7b"
    ]

    for model_name in fallback_models:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": user_input}],
                temperature=0.7,
                max_tokens=256
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"⚠️ Model {model_name} failed: {e}")
            continue

    return "⚠️ All fallback models failed."

# -------------------------------
# Text-to-Speech
# -------------------------------
def speak_text(text: str):
    """Convert AI text reply to speech using gTTS."""
    try:
        tts = gTTS(text)
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_path.name)
        st.audio(temp_path.name, format="audio/mp3")
    except Exception as e:
        st.error(f"⚠️ TTS Error: {e}")

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="SafeCompanion.AI", page_icon="🛡️")

st.title("🛡️ SafeCompanion.AI Prototype")
st.write("A safe, conversational AI prototype powered by Groq API with Text-to-Speech.")

# Enable Text-to-Speech
enable_tts = st.checkbox("🔊 Enable Text-to-Speech")

# Initialize state
if "history" not in st.session_state:
    st.session_state.history = []
if "safe_count" not in st.session_state:
    st.session_state.safe_count = 0
if "unsafe_count" not in st.session_state:
    st.session_state.unsafe_count = 0
if "pii_count" not in st.session_state:
    st.session_state.pii_count = 0

# Chat input
st.subheader("💬 Chat")
user_input = st.text_input("Enter your message:")

if user_input:
    clean_input, flagged, pii_detected = apply_safety_filters(user_input)
    ai_reply = generate_reply(clean_input)

    # Show conversation
    st.markdown(f"👤 **You:** {user_input}")
    st.markdown(f"🤖 **SafeCompanion.AI:** {ai_reply}")

    # Play TTS
    if enable_tts:
        speak_text(ai_reply)

    # Update safety stats
    if flagged:
        st.session_state.unsafe_count += 1
    else:
        st.session_state.safe_count += 1
    if pii_detected:
        st.session_state.pii_count += 1

    # Save history
    st.session_state.history.append({"user": user_input, "ai": ai_reply})

# -------------------------------
# Safety Dashboard
# -------------------------------
st.subheader("📊 Safety Dashboard")
total = st.session_state.safe_count + st.session_state.unsafe_count
if total > 0:
    safe_percent = (st.session_state.safe_count / total) * 100
    unsafe_percent = (st.session_state.unsafe_count / total) * 100
else:
    safe_percent, unsafe_percent = 0, 0

st.write(f"✅ {safe_percent:.0f}% safe interactions detected.")
st.write(f"⚠️ {unsafe_percent:.0f}% flagged as unsafe.")
st.write(f"🔒 {st.session_state.pii_count} private details hidden.")
