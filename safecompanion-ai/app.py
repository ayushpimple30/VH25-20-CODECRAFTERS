import streamlit as st
from transformers import pipeline
from gtts import gTTS
import re
import base64
import os

# Load Hugging Face model
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

model = load_model()

# Safety filter function
def apply_safety_filters(user_input):
    bad_words = ["stupid", "idiot", "fuck", "shit"]
    for word in bad_words:
        if word in user_input.lower():
            return "[filtered]"
    user_input = re.sub(r"\b\d{10,}\b", "[hidden-phone]", user_input)  # Hide phone
    user_input = re.sub(r"\S+@\S+\.\S+", "[hidden-email]", user_input)  # Hide email
    return user_input

# Math detection
def check_math(user_input):
    try:
        if re.match(r"^[0-9+\-*/(). ]+$", user_input):
            return str(eval(user_input))
    except:
        return None
    return None

# Generate AI reply with history
def generate_reply(user_input):
    clean_input = apply_safety_filters(user_input)
    if clean_input != user_input:
        return clean_input

    math_result = check_math(user_input)
    if math_result is not None:
        return math_result

    # Build context from history
    history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in st.session_state["history"]])
    prompt = f"{history_text}\nUser: {clean_input}\nAI:"

    response = model(prompt, max_length=150, do_sample=True, temperature=0.7)[0]['generated_text']
    return response.strip()

# Text to Speech
def text_to_speech(text, filename="tts_output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    return f'<audio autoplay controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# Streamlit UI
st.title("🛡️ SafeCompanion.AI Prototype")
st.write("A safe, conversational AI prototype with Text-to-Speech and Memory")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

enable_tts = st.checkbox("Enable Voice")

st.subheader("💬 Chat")
user_input = st.text_input("Enter your message:")

if user_input:
    st.markdown(f"👤 You: {user_input}")
    ai_reply = generate_reply(user_input)

    # Save to history
    st.session_state["history"].append({"user": user_input, "ai": ai_reply})

    st.markdown(f"🤖 SafeCompanion.AI: {ai_reply}")

    if enable_tts and ai_reply not in ["[filtered]", "[hidden-phone]", "[hidden-email]"]:
        st.markdown(text_to_speech(ai_reply), unsafe_allow_html=True)

# Safety Dashboard
st.subheader("📊 Safety Dashboard")
st.write(f"✅ {len(st.session_state['history'])} safe interactions detected.")
