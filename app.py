
import streamlit as st
from models.llm import query_openai
from models.embeddings import get_embedding
from utils.file_reader import read_code_files
from utils.rag_retriever import CodeRAGRetriever
from utils.web_search import live_search

st.set_page_config(page_title="CodeExplain AI")
st.title("🧠 CodeExplain AI – Understand Legacy Code")

mode = st.selectbox("Choose response mode", ["concise", "detailed"])
uploaded_files = st.file_uploader("Upload code files", type=["py", "js", "java", "txt", "md"], accept_multiple_files=True)
question = st.text_input("Ask something about the code:")

if uploaded_files and question:
    st.info("Processing files...")
    content = read_code_files(uploaded_files)
    chunks = content.split("\n\n")
    retriever = CodeRAGRetriever()
    retriever.add_chunks(chunks)
    context = "\n\n".join(retriever.query(question))

    full_prompt = f"Here is some code context:\n{context}\n\nUser question: {question}"
    response = query_openai(full_prompt, mode=mode)

    if "[Error" in response:
        st.warning("LLM failed. Using web search instead.")
        response = live_search(question)

    st.markdown(f"### Response:\n{response}")
