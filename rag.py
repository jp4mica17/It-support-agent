"""
rag.py — RAG retrieval layer

Wraps ChromaDB to provide semantic search over the IT knowledge base.
Uses sentence-transformers (all-MiniLM-L6-v2) for local, free embeddings.
"""

import chromadb
from chromadb.utils import embedding_functions


class RAGRetriever:
    """Semantic search over the IT knowledge base stored in ChromaDB."""

    COLLECTION_NAME = "it_knowledge_base"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    def __init__(self, db_path: str = "./chroma_db"):
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.EMBEDDING_MODEL
        )
        self.client = chromadb.PersistentClient(path=db_path)

        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"},
        )

    def is_ready(self) -> bool:
        """Return True if the KB has been ingested."""
        return self.collection.count() > 0

    def search(self, query: str, n_results: int = 3) -> list[dict]:
        """
        Search the knowledge base for chunks relevant to `query`.

        Returns a list of dicts with keys: title, content, score, article_id.
        Scores are cosine similarity (0–1, higher = more relevant).
        """
        count = self.collection.count()
        if count == 0:
            return []

        n_results = min(n_results, count)

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        articles = []
        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            score = max(0.0, 1.0 - distance)  # cosine distance → similarity

            articles.append(
                {
                    "title": results["metadatas"][0][i].get("title", "KB Article"),
                    "content": results["documents"][0][i],
                    "score": round(score, 3),
                    "article_id": results["metadatas"][0][i].get("article_id", ""),
                }
            )

        return articles
