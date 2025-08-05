
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    try:
        return model.encode(text)
    except Exception as e:
        print("Embedding error:", e)
        return None
