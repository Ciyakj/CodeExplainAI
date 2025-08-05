import streamlit as st
from models.llm import call_llm
from models.embeddings import get_embedding
from utils.file_reader import read_code_files
from utils.rag_retriever import CodeRAGRetriever
from utils.web_search import live_search

# Page configuration
st.set_page_config(page_title="CodeExplain AI")
st.title("🧠 CodeExplain AI – Understand Legacy Code")

# Mode selector
mode = st.selectbox("Choose response mode", ["concise", "detailed"])

# File uploader
uploaded_files = st.file_uploader(
    "Upload code files",
    type=["py", "js", "java", "txt", "md"],
    accept_multiple_files=True
)

# Question input
question = st.text_input("Ask something about the code:")

if uploaded_files and question:
    try:
        st.info("Processing files...")

        # Read all uploaded files
        content = read_code_files(uploaded_files)

        # Split into chunks
        chunks = content.split("\n\n")

        # RAG Retriever
        retriever = CodeRAGRetriever()
        retriever.add_chunks(chunks)
        context = "\n\n".join(retriever.query(question))

        # Form final prompt
        full_prompt = f"""
You are CodeExplain AI.

Here is some legacy code context:
{context}

The user asked (in {mode} mode): {question}

Respond accordingly.
"""

        # Get LLM response
        response = call_llm(full_prompt)

        # Fallback if LLM fails
        if "[Error" in response or response.strip() == "":
            st.warning("LLM failed. Using web search instead.")
            response = live_search(question)

        # Output
        st.markdown("### 🧠 Response")
        st.write(response)

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")

elif question and not uploaded_files:
    st.warning("Please upload at least one code file.")
