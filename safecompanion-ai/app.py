# app.py
import streamlit as st
from detoxify import Detoxify
import re
import spacy
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="SafeCompanion.AI", page_icon="🛡️")
st.title("🛡️ SafeCompanion.AI Prototype")

# --- Load spaCy model for PII detection ---
nlp = spacy.load("en_core_web_sm")

# --- Use Flan-T5 (instruction-tuned, safer for demos) ---
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# --- Safety Classifiers ---
toxicity_check = Detoxify("original")

# --- Crisis Keywords ---
CRISIS_KEYWORDS = [
    "worthless", "suicide", "kill myself",
    "end my life", "harm myself", "self harm",
    "depressed", "i want to die"
]

# --- Helper functions ---
PROFANITY_WORDS = ["badword", "fuck", "shit", "bitch"]

def contains_profanity(text: str) -> bool:
    return re.search(r"\b(" + "|".join(PROFANITY_WORDS) + r")\b", text.lower()) is not None

def is_toxic(text: str) -> bool:
    return toxicity_check.predict(text)["toxicity"] > 0.7

def is_crisis(text: str) -> bool:
    return any(keyword in text.lower() for keyword in CRISIS_KEYWORDS)

def scrub_pii(text: str) -> (str, bool):
    """Detect and redact PII, return cleaned text and flag if redaction happened"""
    doc = nlp(text)
    redacted = text
    pii_found = False
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "ORG", "CARDINAL", "DATE", "TIME", "MONEY"]:
            redacted = redacted.replace(ent.text, "[REDACTED]")
            pii_found = True
    if re.search(r"\b[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", redacted):
        redacted = re.sub(r"\b[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL REDACTED]", redacted)
        pii_found = True
    if re.search(r"\b\d{10}\b", redacted):
        redacted = re.sub(r"\b\d{10}\b", "[PHONE REDACTED]", redacted)
        pii_found = True
    return redacted, pii_found

def clean_response(text: str) -> str:
    """Clean AI output: remove spammy symbols, links, and repetitions"""
    text = re.sub(r"[\:\)\]\(]{2,}", " ", text)       # Remove symbol spam
    text = re.sub(r"\d{4,}", "", text)                # Remove digit spam
    text = re.sub(r"http\S+|www\.\S+", "", text)      # Remove hallucinated links
    text = re.sub(r"address\:.*", "", text)
    text = re.sub(r"([!?.])\1{2,}", r"\1", text)      # Collapse punctuation

    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 2]

    if not sentences:
        return "I'm here to chat with you. How are you feeling today?"

    return " ".join(sentences[:3]).strip()

def ask_ai(prompt: str) -> str:
    """Send input to Flan-T5 and return cleaned response"""
    try:
        wrapped = f"The user said: '{prompt}'. Reply in a supportive and conversational way."
        result = generator(
            wrapped,
            max_length=150,
            min_length=20,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=2.0
        )
        return clean_response(result[0]["generated_text"])
    except Exception as e:
        return f"⚠️ AI model error: {str(e)}"

# --- UI with guardrails (adjust, not replace) ---
user_input = st.text_input("Enter your message:")

if user_input:
    clean_input, pii_flag = scrub_pii(user_input)
    ai_response = ask_ai(clean_input)

    # Fallback for nonsense
    if not ai_response or len(ai_response.split()) < 3:
        ai_response = "I'm here to chat with you. How are you feeling today?"

    # Adjust responses with guardrails
    if contains_profanity(user_input):
        ai_response = "⚠️ I noticed some harsh language. Let's try to keep things kind 🙂. " + ai_response

    if is_toxic(user_input):
        ai_response = "⚠️ Your message sounded a bit toxic. I’ll still respond kindly: " + ai_response

    if is_crisis(user_input):
        ai_response = ("⚠️ It sounds like you're going through something serious. "
                       "You're not alone — please reach out to someone you trust or call a helpline for support. "
                       + " Here's me still listening: " + ai_response)

    if pii_flag:
        ai_response = "ℹ️ For privacy, I’ve hidden sensitive details. " + ai_response

    # Display final safe response
    st.write("✅ Safe message accepted.")
    st.write("AI Response:", ai_response)
