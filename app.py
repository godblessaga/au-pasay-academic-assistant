import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="AU Pasay AI Academic Assistant", page_icon="🎓")
st.title("🎓 AU Pasay AI Academic Assistant")
st.caption("Arellano University Pasay - Student Academic Advising Chatbot")

# Load knowledge base text file
@st.cache_data
def load_knowledge_base():
    if os.path.exists("all_handbooks.txt"):
        with open("all_handbooks.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

KNOWLEDGE_BASE = load_knowledge_base()

# Initialize Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY environment variable is missing!")
    st.stop()

client = genai.Client(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
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

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    http_options=types.HttpOptions(
                        retry_options=types.HttpRetryOptions(
                            attempts=5,
                            initial_delay=1.0,
                            http_status_codes=[503, 429, 500, 502, 504]
                        )
                    )
                )
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error generating response: {e}")
