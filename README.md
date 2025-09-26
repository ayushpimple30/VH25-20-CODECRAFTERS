# 🛡️ SafeCompanion.AI

**SafeCompanion.AI** is an AI-powered chatbot designed to provide **safe, supportive, and responsible interactions**.
It is built as part of the **VCET Hackathon 2025 (Security Domain)** with the goal of designing **guardrails for AI companions**.

---

## ✨ Features

* 🔍 **Input Filtering** – blocks profanity, toxicity, PII (phone numbers, emails, etc.)
* ✅ **Output Validation** – prevents hallucinations, ensures safe and factual responses
* 🛡️ **Privacy Protection** – sensitive data is scrubbed and hidden automatically
* 🔑 **Role-Based Access** – supports access controls and policies
* 📜 **Audit Trails** – strong logging and monitoring of all interactions
* 💬 **Friendly Companion** – conversational, empathetic, and supportive AI

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ayushpimple30/safecompanion-ai.git
cd safecompanion-ai
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate   # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a `.env` file in the project root and add your Hugging Face API key:

```
HF_API_KEY=your_huggingface_api_key
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 📸 Demo

*(Optional: Add a screenshot of your app here)*

```markdown
![SafeCompanion.AI Screenshot](assets/screenshot.png)
```

---

## 🏆 Hackathon Context

This project was developed for the **VCET Hackathon 2025 (Security Domain)**.
The challenge: *“Develop guardrails for AI models used in AI companions.”*

SafeCompanion.AI directly addresses this by combining **LLM-powered conversation** with **robust safety filters**.

---

## 📂 Project Structure

```
safecompanion-ai/
│-- app.py             # Main Streamlit app
│-- requirements.txt   # Dependencies
│-- .env               # API keys (ignored in GitHub)
│-- .gitignore         # Ignore rules
│-- LICENSE            # MIT License
```

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Team

**Team CodeCrafters (VH25-20)**

* Ayush Pimple (@ayushpimple10)
* Shivanshu
* Harsh
* Shervin
