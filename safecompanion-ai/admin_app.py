import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SafeCompanion.AI Admin", page_icon="🛡️", layout="centered")

st.title("🛡️ SafeCompanion.AI – Admin Tracker")
st.caption("Monitor chatbot activity logs in real-time. No user personal details are stored.")

log_file = "activity_log.csv"

if os.path.exists(log_file):
    df = pd.read_csv(log_file)

    if not df.empty:
        st.subheader("📜 Recent Activity Logs")
        st.dataframe(df.tail(20), use_container_width=True)

        st.subheader("📊 Stats Overview")
        safe = df["safe_flag"].sum()
        unsafe = len(df) - safe
        pii = df["pii_flag"].sum()

        st.metric("✅ Safe Interactions", safe)
        st.metric("⚠️ Unsafe Interactions", unsafe)
        st.metric("🔒 PII Hidden", pii)

    else:
        st.warning("No activity logs found yet.")
else:
    st.warning("No activity_log.csv file found. Start using the chatbot to generate logs.")
