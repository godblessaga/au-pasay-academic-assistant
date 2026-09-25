import os
import streamlit as st
from google import genai

# Page Setup
st.set_page_config(page_title="AU Pasay AI Academic Assistant", page_icon="🎓")
st.title("🎓 AU Pasay AI Academic Assistant")
st.caption("Arellano University Pasay - Student Academic Advising Chatbot")

# Load your combined text document
@st.cache_resource
def load_knowledge_base():
    try:
        with open("all_handbooks.txt", "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return "AU Pasay General Academic Rules and Guidelines."

KNOWLEDGE_BASE = load_knowledge_base()

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Manage Session Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if prompt := st.chat_input("Ask about courses, enrollment, or academic policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_prompt = f"""
        You are the official AI Academic Assistant for Arellano University Pasay.
        Answer the student's question accurately based strictly on the university documentation provided below.

        === UNIVERSITY KNOWLEDGE BASE ===
        {KNOWLEDGE_BASE}
        =================================

        Student Question: {prompt}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})