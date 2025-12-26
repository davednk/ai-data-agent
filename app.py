import streamlit as st
import pandas as pd
import google.generativeai as genai
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. ACCESS CONTROL ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

if not st.session_state.password_correct:
    st.title("🔒 Access Restricted")
    pwd = st.text_input("Enter your 4-digit code", type="password")
    if st.button("Unlock"):
        if pwd == st.secrets["APP_PASSWORD"]:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Wrong code. Try again.")
    st.stop()

# --- 2. AI AGENT SETUP ---
# This pulls the long Google key from your hidden Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)
except Exception:
    st.error("API Key Missing: Check your Streamlit Secrets dashboard.")
    st.stop()

st.title("🤖 AI Data Science Agent")
# ... rest of your file upload and agent.run(query) code ...
