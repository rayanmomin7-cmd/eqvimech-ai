# import chromadb
# from sentence_transformers import SentenceTransformer

# client = chromadb.PersistentClient(path="db")
# collection = client.get_collection("eqvimech")
# embed_model = SentenceTransformer("all-MiniLM-L6-v2")
import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader

# =========================

# LOAD PDFS

# =========================

def load_pdfs():
    pdf_text = ""
    pdf_folder = "pdfs"
    if os.path.exists(pdf_folder):
        for file in os.listdir(pdf_folder):
            if file.endswith(".pdf"):
                try:
                    pdf_path = os.path.join(pdf_folder, file)
                    reader = PdfReader(pdf_path)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            pdf_text += f"\n\nFILE: {file}\n"
                            pdf_text += text
                except Exception:
                    pass
    return pdf_text


# =========================

# API KEY

# =========================

import os

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

context = load_pdfs()


# =========================

# PAGE SETTINGS

# =========================

st.set_page_config(
page_title="Eqvimech AI Assistant",
page_icon="🤖",
layout="wide"
)

# =========================

# CUSTOM CSS

# =========================

st.markdown("""

<style>

.user-msg {
    background-color: #2196F3;
    color: white;
    padding: 12px;
    border-radius: 15px;
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 30%;
    text-align: right;
    font-size: 16px;
}

.bot-msg {
    background-color: #4CAF50;
    color: white;
    padding: 12px;
    border-radius: 15px;
    margin-top: 10px;
    margin-bottom: 10px;
    margin-right: 30%;
    text-align: left;
    font-size: 16px;
}

</style>

""", unsafe_allow_html=True)

# =========================

# HEADER

# =========================

col1, col2 = st.columns([1,4])

with col1:
    st.image("logo.jpeg", width=130)

with col2:
    st.markdown(""" <h1 style='margin-top:15px;'>
    Eqvimech AI Assistant 🤖 </h1>
    <p>
    Internal AI Assistant for Testing Machines
    </p>
    """, unsafe_allow_html=True)

st.divider()

# =========================

# CLEAR CHAT

# =========================

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# =========================

# MEMORY

# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================

# SHOW OLD MESSAGES

# =========================

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="user-msg">
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="bot-msg">
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================

# INPUT BOX

# =========================

prompt = st.chat_input("Ask your question")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

conversation = "\n".join(
    [f"{m['role']}: {m['content']}"
     for m in st.session_state.messages[-6:]]
)
        # Last 6 messages only
conversation = "\n".join(
    [f"{m['role']}: {m['content']}"
     for m in st.session_state.messages[-6:]]
)


full_prompt = f"""
You are Eqvimech AI Assistant.

Use ONLY the information below if relevant.

Context:
{context}

Conversation:
{conversation}

Answer clearly and professionally.
"""

with st.spinner("""
📄 Reading Technical Documents...
🔍 Searching Knowledge Base...
🤖 Generating Response...
"""):
        response = model.generate_content(full_prompt)

    answer = response.text

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # st.rerun()


