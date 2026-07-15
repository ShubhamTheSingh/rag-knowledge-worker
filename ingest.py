"""Ingestion: turn the knowledge-base documents into a searchable vector store.

Pipeline:  load docs -> split into chunks -> embed each chunk -> store in Chroma.
Run once (and re-run whenever the knowledge base changes):  python ingest.py
"""
import os
import shutil

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

import config

load_dotenv(override=True)


def load_documents():
    """Read every markdown file in the knowledge base."""
    loader = DirectoryLoader(
        config.KNOWLEDGE_BASE_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    # Keep just the filename as the source (used later for citations).
    for d in docs:
        d.metadata["source"] = os.path.basename(d.metadata.get("source", "unknown"))
    return docs


def build_vector_store():
    """Load -> split -> embed -> persist. Returns the Chroma store."""
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)

    # Rebuild from scratch so re-running is deterministic.
    if os.path.exists(config.VECTOR_STORE_DIR):
        shutil.rmtree(config.VECTOR_STORE_DIR)

    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.COLLECTION_NAME,
        persist_directory=config.VECTOR_STORE_DIR,
    )
    print(f"Ingested {len(docs)} document(s) -> {len(chunks)} chunk(s) "
          f"into '{config.VECTOR_STORE_DIR}'.")
    return store


if __name__ == "__main__":
    build_vector_store()
