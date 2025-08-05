import streamlit as st
import os
from models.llm import call_llm
from models.embeddings import get_embedding
from utils.file_reader import read_code_files
from utils.rag_retriever import CodeRAGRetriever
from utils.web_search import live_search

# Page configuration
st.set_page_config(page_title="CodeExplain AI")
st.title("🧠 CodeExplain AI – Understand Legacy Code")

# Sidebar options
st.sidebar.header("🔧 Settings")
mode = st.sidebar.radio("Choose response mode", ["concise", "detailed"])
model = st.sidebar.radio("Choose LLM model", ["groq", "gemini", "deepseek"])

# File uploader
uploaded_files = st.file_uploader(
    "Upload code files",
    type=["py", "js", "java", "txt", "md"],
    accept_multiple_files=True
)

# User question input
question = st.text_input("Ask something about the code:")

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

if uploaded_files and question:
    try:
        st.info("Processing files...")

        # Read and chunk the code files
        content = read_code_files(uploaded_files)
        chunks = content.split("\n\n")
        retriever = CodeRAGRetriever()
        retriever.add_chunks(chunks)
        context = "\n\n".join(retriever.query(question))

        # Format the prompt
        prompt = f"""
You are CodeExplain AI.
Here is some legacy code context:
{context}

The user asked (in {mode} mode): {question}
Respond accordingly.
"""

        # Get LLM response
        response = call_llm(prompt, model)

        if not isinstance(response, str) or response.strip() == "":
            st.warning("LLM failed or returned empty. Trying web search.")
            response = live_search(question)

        # Display answer
        st.markdown("### 🧠 Response")
        st.write(response)

        # Show the source code chunks
        with st.expander("🔍 View relevant code context used"):
            st.code(context)

        # Download button
        st.download_button("💾 Download Response", response, file_name="response.txt")

        # Store in history
        st.session_state.history.append((question, response))

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")

elif question and not uploaded_files:
    st.warning("Please upload at least one code file.")

# Optional: display previous Q&A
if st.session_state.history:
    with st.expander("🕓 View past questions and answers"):
        for i, (q, r) in enumerate(st.session_state.history[::-1]):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"**A{i+1}:** {r}")
