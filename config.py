"""Configuration for the RAG Knowledge Worker.

All tunables live here so the pipeline code stays clean and the behaviour is
easy to reason about (and to explain in an interview).
"""
import os

# --- Models ----------------------------------------------------------------
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")             # answers questions
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")  # cheap, strong

# --- Paths -----------------------------------------------------------------
KNOWLEDGE_BASE_DIR = os.getenv("KNOWLEDGE_BASE_DIR", "knowledge-base")
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vector_store")  # Chroma persists here
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_base")

# --- Chunking --------------------------------------------------------------
# Documents are split into overlapping chunks so retrieval is granular but
# chunks keep enough surrounding context to stay meaningful.
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))     # characters per chunk
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))  # overlap between chunks

# --- Retrieval -------------------------------------------------------------
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "4"))  # how many chunks to feed the LLM
