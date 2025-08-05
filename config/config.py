import os

# Load API keys and settings from Streamlit secrets or environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini")  # Options: gemini, deepseek
RESPONSE_MODE = os.getenv("RESPONSE_MODE", "detailed")  # Options: concise, detailed
