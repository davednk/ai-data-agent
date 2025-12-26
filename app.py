import streamlit as st
import pandas as pd
import google.generativeai as genai
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. SECURITY (Password)
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True
    
    pwd = st.sidebar.text_input("Enter Password", type="password")
    if st.sidebar.button("Unlock"):
        if pwd == "your_password": # Set your password here
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.sidebar.error("Wrong password")
    return False

if not check_password():
    st.title("🔒 App Locked")
    st.stop()

# 2. SETUP
API_KEY = "AIzaSyAv3GRjjJypWmC6Kg3JzUgSHrmjS-v9-cY"
genai.configure(api_key=API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)

st.title("🤖 AI Data Science Agent")

uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.write("Data Preview:", df.head())
    
    # 3. THE AGENT
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
    
    query = st.text_input("What should the AI Agent do? (e.g., 'Clean nulls and plot a chart')")
    if st.button("Run Agent"):
        with st.spinner("Agent is working..."):
            response = agent.run(query)
            st.success("Finished!")
            st.write(response)
