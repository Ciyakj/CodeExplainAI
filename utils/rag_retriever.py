
import faiss
import numpy as np
from models.embeddings import get_embedding

class CodeRAGRetriever:
    def __init__(self):
        self.embeddings = []
        self.chunks = []
        self.index = faiss.IndexFlatL2(384)

    def add_chunks(self, chunks):
        self.chunks = chunks
        vectors = [get_embedding(c) for c in chunks]
        self.embeddings = np.array(vectors).astype("float32")
        self.index.add(self.embeddings)

    def query(self, question, top_k=3):
        query_emb = np.array([get_embedding(question)]).astype("float32")
        distances, indices = self.index.search(query_emb, top_k)
        return [self.chunks[i] for i in indices[0]]
