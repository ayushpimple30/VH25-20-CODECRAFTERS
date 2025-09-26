# 🛡️ SafeCompanion.AI

SafeCompanion.AI is an AI-powered chatbot designed for **safe, supportive, and responsible interactions**.  
It implements guardrails such as:
- ✅ Input filtering (toxicity, profanity, PII detection)
- ✅ Output filtering (hallucination control, safe responses)
- ✅ Privacy protection (scrubbing phone numbers, emails, addresses)
- ✅ Logging & audit trails for monitoring

---

## 🚀 Features
- Built using **Python + Streamlit**
- Uses **Hugging Face models** for AI responses
- Protects against unsafe or harmful outputs
- Supports role-based access and audit logs

---

## ⚙️ Setup Instructions
1. Clone the repo:
   ```bash
   git clone https://github.com/ayushpimple30/safecompanion-ai.git
   cd safecompanion-ai

Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # Mac/Linux


Install dependencies:

pip install -r requirements.txt


Create a .env file and add your API keys:

HF_API_KEY=your_huggingface_api_key


Run the app:

streamlit run app.py
