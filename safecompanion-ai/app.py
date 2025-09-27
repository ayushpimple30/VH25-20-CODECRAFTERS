import os
import streamlit as st
from groq import Groq
import pytesseract
from PIL import Image


from safety import apply_safety_filters
from tts import speak_text
from activity_logger import log_activity


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Please set it with: setx GROQ_API_KEY 'your_key_here'")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


st.set_page_config(page_title="SafeCompanion.AI Prototype", layout="wide")

st.title("🛡️ SafeCompanion.AI Prototype")
st.caption("A safe, conversational AI prototype powered by Groq API with Guardrails, Text-to-Speech, Image Upload, and Activity Tracking.")


st.sidebar.header("⚙️ Settings")
enable_tts = st.sidebar.checkbox("Enable Voice Replies")
language = st.sidebar.selectbox("🌐 Select Language for Speech Output", ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Gujarati", "Punjabi"])


def generate_reply(user_input: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are a safe AI assistant. Always reply politely, safely, and responsibly."},
                {"role": "user", "content": user_input},
            ],
        )

        if hasattr(response.choices[0].message, "content"):
            return response.choices[0].message.content.strip()
        elif isinstance(response.choices[0].message, dict):
            return response.choices[0].message.get("content", "").strip()
        else:
            return "⚠️ Could not parse AI reply."
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"


def extract_text_from_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[OCR Error: {str(e)}]"


uploaded_file = st.file_uploader("📤 Or upload an image", type=["png", "jpg", "jpeg"])
user_input = st.text_input("💬 Enter your message:")

if st.button("🚀 Send"):
    if uploaded_file:
        extracted_text = extract_text_from_image(uploaded_file)
        st.write("📖 Extracted from Image:", extracted_text)
        user_input = extracted_text

    if user_input.strip():
        
        clean_input, flagged_in, pii_in = apply_safety_filters(user_input)

        if flagged_in or pii_in:
            st.warning("⚠️ Your input contained unsafe or private details and was blocked.")
            log_activity(user_input, "[BLOCKED]", flagged_in, pii_in, blocked=True)
        else:
           
            ai_reply = generate_reply(clean_input)

          
            ai_reply, flagged_out, pii_out = apply_safety_filters(ai_reply)

            st.markdown(f"🤖 **SafeCompanion.AI**: {ai_reply}")

          
            if enable_tts and ai_reply.strip():
                audio_file = speak_text(ai_reply, lang="en")
                st.audio(audio_file, format="audio/mp3")

          
            if "safe_count" not in st.session_state:
                st.session_state.safe_count = 0
                st.session_state.unsafe_count = 0
                st.session_state.pii_count = 0

            if flagged_out:
                st.session_state.unsafe_count += 1
            else:
                st.session_state.safe_count += 1
            if pii_out:
                st.session_state.pii_count += 1

            
            log_activity(user_input, ai_reply, flagged_out, pii_out, blocked=False)


st.subheader("📊 Safety Dashboard")

total = st.session_state.get("safe_count", 0) + st.session_state.get("unsafe_count", 0)

if total > 0:
    st.write(f"✅ {st.session_state.safe_count} safe interactions detected.")
    st.write(f"⚠️ {st.session_state.unsafe_count} flagged as unsafe.")
    st.write(f"🔒 {st.session_state.pii_count} private details hidden.")
else:
    st.info("No interactions yet.")
