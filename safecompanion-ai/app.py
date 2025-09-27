import streamlit as st
from transformers import pipeline
import re

# --------------------------
# Safety Filters
# --------------------------
BAD_WORDS = {"fuck", "stupid", "idiot", "bitch", "kill", "suicide"}
PII_PATTERNS = [
    r"\b\d{10}\b",  # phone number
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",  # email
]

def clean_input(user_input: str) -> str:
    # Block harmful words
    for bad in BAD_WORDS:
        if bad in user_input.lower():
            return "[Content removed for safety]"
    
    # Redact PII
    for pattern in PII_PATTERNS:
        user_input = re.sub(pattern, "[REDACTED]", user_input)
    
    return user_input

# --------------------------
# Load Models
# --------------------------
@st.cache_resource
def load_model(model_choice):
    return pipeline("text2text-generation", model=model_choice)

# --------------------------
# Reply Generator
# --------------------------
def generate_reply(model, history, user_input):
    # Math check
    if re.match(r"^\d+\s*[\+\-\*/]\s*\d+$", user_input):
        try:
            result = eval(user_input)
            return f"The result is {result}"
        except Exception:
            return "I couldn’t calculate that safely."
    
    # Prepare context
    context = " ".join([f"User: {u} AI: {a}" for u, a in history[-5:]])
    prompt = f"{context} User: {user_input} AI:"
    
    # Generate
    response = model(prompt, max_length=150, do_sample=True, temperature=0.7)[0]['generated_text']
    
    # Clean response
    response = response.split("AI:")[-1].strip()
    
    return response

# --------------------------
# Streamlit App
# --------------------------
st.set_page_config(page_title="SafeCompanion.AI", page_icon="🛡️", layout="wide")

st.title("🛡️ SafeCompanion.AI Prototype")
st.caption("A safe, conversational AI prototype powered by Hugging Face.")

model_choice = st.sidebar.selectbox(
    "Choose AI Model",
    ["google/flan-t5-base", "facebook/blenderbot-400M-distill"]
)

# Load chosen model
model = load_model(model_choice)

if "history" not in st.session_state:
    st.session_state["history"] = []
if "safe_count" not in st.session_state:
    st.session_state["safe_count"] = 0
if "unsafe_count" not in st.session_state:
    st.session_state["unsafe_count"] = 0

user_input = st.text_input("Enter your message:")

if user_input:
    clean_user_input = clean_input(user_input)

    if clean_user_input == "[Content removed for safety]":
        ai_reply = "⚠️ That message was blocked for safety reasons."
        st.session_state["unsafe_count"] += 1
    else:
        ai_reply = generate_reply(model, st.session_state["history"], clean_user_input)
        st.session_state["safe_count"] += 1
    
    st.session_state["history"].append((user_input, ai_reply))
    
    st.write(f"👤 You: {user_input}")
    st.write(f"🤖 SafeCompanion.AI: {ai_reply}")

# --------------------------
# Safety Dashboard
# --------------------------
st.subheader("📊 Safety Dashboard")
total = st.session_state["safe_count"] + st.session_state["unsafe_count"]
safe_pct = (st.session_state["safe_count"] / total) * 100 if total > 0 else 0
unsafe_pct = 100 - safe_pct

st.metric("✅ Safe Interactions", f"{safe_pct:.0f}%")
st.metric("⚠️ Unsafe Interactions", f"{unsafe_pct:.0f}%")
