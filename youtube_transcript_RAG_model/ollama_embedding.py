from typing import List
import requests
from langchain.embeddings.base import Embeddings

class MyLocalOllamaEmbeddings(Embeddings):
    def __init__(self, model: str = "nomic-embed-text", url = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.url =url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)

    def _embed(self, text: str) -> List[float]:
        response = requests.post(
            self.url,
            json={"model": self.model, "prompt": text}
        )

        response.raise_for_status()

        return response.json()["embedding"]