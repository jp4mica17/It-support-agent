"""
ingest.py — Knowledge Base Ingestion

Reads all Markdown files from ./kb/, chunks them, embeds with
sentence-transformers, and stores in ChromaDB.

Run once before starting the app:
    python ingest.py

Re-run any time you add or update KB articles.
"""

import glob
import os

import chromadb
from chromadb.utils import embedding_functions


KB_DIR = "./kb"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "it_knowledge_base"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 600   # characters per chunk
CHUNK_OVERLAP = 80  # characters of overlap between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks, preferring sentence boundaries.
    Shorter texts are returned as a single chunk.
    """
    if len(text) <= chunk_size:
        return [text.strip()]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            # Try to break at the last sentence boundary within the window
            boundary = text.rfind(".", start, end)
            if boundary > start + chunk_size // 2:
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap

    return chunks


def load_article(filepath: str) -> tuple[str, str]:
    """
    Parse a Markdown KB article.
    Returns (title, body) where title comes from the first # heading.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    lines = content.split("\n")
    if lines and lines[0].startswith("#"):
        title = lines[0].lstrip("#").strip()
        body = "\n".join(lines[1:]).strip()
    else:
        title = os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()
        body = content

    return title, body


def ingest():
    print("🔍  Scanning KB articles…")
    filepaths = sorted(glob.glob(os.path.join(KB_DIR, "*.md")))
    if not filepaths:
        print(f"⚠️  No .md files found in {KB_DIR}/. Add articles and re-run.")
        return

    print(f"📄  Found {len(filepaths)} articles. Loading embeddings model (first run may download ~80 MB)…")

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=DB_PATH)

    # Wipe and recreate the collection for a clean ingest
    try:
        client.delete_collection(COLLECTION_NAME)
        print("🗑️   Cleared existing collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    documents, metadatas, ids = [], [], []
    total_chunks = 0

    for article_idx, filepath in enumerate(filepaths):
        title, body = load_article(filepath)
        chunks = chunk_text(body)

        for chunk_idx, chunk in enumerate(chunks):
            chunk_id = f"kb_{article_idx:03d}_chunk_{chunk_idx:03d}"
            documents.append(chunk)
            metadatas.append(
                {
                    "title": title,
                    "article_id": f"kb_{article_idx:03d}",
                    "filepath": filepath,
                    "chunk_index": chunk_idx,
                }
            )
            ids.append(chunk_id)
            total_chunks += 1

        print(f"  ✅  [{article_idx + 1}/{len(filepaths)}] {title} — {len(chunks)} chunk(s)")

    collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print(f"\n🎉  Done! Ingested {len(filepaths)} articles ({total_chunks} chunks) into ChromaDB.")
    print(f"     DB stored at: {os.path.abspath(DB_PATH)}/")
    print("\nNow run the app:  streamlit run app.py")


if __name__ == "__main__":
    ingest()
