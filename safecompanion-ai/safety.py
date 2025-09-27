import re

# Expanded toxic / harmful keywords
TOXIC_WORDS = [
    "fuck", "shit", "bitch", "asshole", "bastard", "slut", "dick", "cunt", "faggot",
    "kill", "suicide", "die", "hurt myself", "end my life", "hate you", "stupid"
]

# Regex for detecting PII (emails, phone numbers, etc.)
PII_PATTERNS = [
    r"\b\d{10}\b",                # phone numbers (10 digits)
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",  # emails
]

def apply_safety_filters(text: str):
    flagged = False
    pii_detected = False
    clean_text = text

    # --- Check for toxic/harmful content ---
    for word in TOXIC_WORDS:
        if re.search(rf"\b{word}\b", clean_text, re.IGNORECASE):
            clean_text = re.sub(rf"\b{word}\b", "[REDACTED]", clean_text, flags=re.IGNORECASE)
            flagged = True

    # --- Check for PII ---
    for pattern in PII_PATTERNS:
        if re.search(pattern, clean_text):
            clean_text = re.sub(pattern, "[REDACTED]", clean_text)
            pii_detected = True

    return clean_text, flagged, pii_detected
