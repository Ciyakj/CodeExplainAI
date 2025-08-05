from langchain_groq import ChatGroq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

def call_llm(prompt):
    try:
        llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)
        return llm.invoke(prompt)
    except Exception as e:
        return f"Groq API Error: {str(e)}"
