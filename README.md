# 🛡️ SafeCompanion.AI

A **safe conversational AI prototype** powered by **Groq API** with strong **guardrails**.
Designed to enable **secure, ethical, and private interactions** with built-in safety features.

---

## ✨ Features

* 🔒 **Guardrails**

  * Input filtering: toxicity, profanity, self-harm, topic restrictions
  * Output validation: prevent hallucinations, enforce safe responses
  * PII detection & scrubbing (emails, phone numbers, etc.)

* 🗣️ **Conversational AI**

  * Text-based chat with Groq LLMs
  * Text-to-Speech (TTS) in multiple languages
  * Optional microphone input for voice queries

* 🖼️ **Image Upload**

  * Upload images (JPG/PNG)
  * Extract text using OCR (Tesseract)

* 📊 **Safety Dashboard**

  * Track safe/unsafe interactions
  * Monitor PII redaction events

* 📜 **Activity Logging**

  * Every interaction stored in `activity_log.csv`
  * Logs include timestamp, input, output, safety flags
  * Audit-ready for compliance

* 🛠️ **Admin Dashboard**

  * Separate app (`admin_app.py`)
  * View logs in a secure interface
  * Reset logs when needed
 


🎥 Demo

Here’s how SafeCompanion.AI looks in action:

Chatbot Demo

User enters a text message or uploads an image.

Unsafe words/PII get redacted automatically.

AI replies safely and can speak the answer (TTS).

Dashboard updates in real-time with safety stats.

Admin Tracker Demo

Admin opens admin_app.py (on port 8502).

Views logged activities with timestamps.

Can reset logs with one click.


<img width="1920" height="1080" alt="Screenshot (77)" src="https://github.com/user-attachments/assets/1e4f9633-aa01-49ca-a28b-9838912fd3d9" />

<img width="1920" height="1080" alt="Screenshot (78)" src="https://github.com/user-attachments/assets/dbffa91f-222f-47c1-abc0-622bf8cdca98" />



---

## 📂 Project Structure

```
safecompanion-ai/
│
├── app.py                # Main chatbot app
├── admin_app.py          # Admin tracker dashboard
├── safety.py             # Guardrails: input/output filtering
├── tts.py                # Text-to-Speech helper
├── activity_logger.py    # Logging system
├── activity_log.csv      # Interaction logs (auto-generated)
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone Repo

```bash
git clone https://github.com/YOUR_USERNAME/safecompanion-ai.git
cd safecompanion-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Groq API Key

```bash
setx GROQ_API_KEY "your_api_key_here"   # Windows
export GROQ_API_KEY="your_api_key_here" # macOS/Linux
```

---

## 🚀 Usage

### Run the Chatbot

```bash
streamlit run app.py
```

### Run the Admin Tracker (separate port)

```bash
streamlit run admin_app.py --server.port 8502
```

---

## 🗑️ Reset Activity Logs

* Open `admin_app.py` in browser → Click **"🗑️ Reset Logs"**
* Or manually clear `activity_log.csv`

---

## 🛡️ Guardrails in Action

* **Profanity/Toxicity:** `fuck you` → `[REDACTED] you`
* **Self-Harm:** `I want to kill myself` → `I want to [REDACTED-SELF-HARM]`
* **PII:**

  * `Email me at test@example.com` → `Email me at [REDACTED-PII]`
  * `Call me at 9876543210` → `Call me at [REDACTED-PII]`

---

## 📊 Safety Dashboard Example

* ✅ 12 safe interactions detected
* ⚠️ 3 flagged as unsafe
* 🔒 2 private details hidden

---

## 🔮 Future Improvements

* Role-based access control for admins
* More advanced PII detection (names, addresses)
* Better contextual toxicity detection (via ML model)
* Secure deployment with HTTPS & user authentication

---

## 👨‍💻 Authors

* **Ayush Pimple** – Project Developer

---

Do you want me to also create a **`.gitignore`** so your `activity_log.csv` and temporary audio files aren’t pushed to GitHub?


## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

