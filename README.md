<div align="center">

# 🔎 RAG Knowledge Worker

**Ask natural-language questions over a document knowledge base — answered with retrieval-augmented generation and source citations.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Chroma](https://img.shields.io/badge/Chroma-VectorDB-6366F1)](https://www.trychroma.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-embeddings%20%2B%20chat-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

> 🚧 **Work in progress** — built incrementally. Full architecture docs, diagram, and demo land as the project is completed.

## What it is
A Retrieval-Augmented Generation (RAG) assistant that answers questions grounded in a set
of documents (here: a sample fintech company knowledge base). Instead of relying on the
model's memory, it **retrieves the most relevant chunks** from a vector database and asks
the LLM to answer **using only those chunks** — so answers stay accurate and cite sources.

## How it works (high level)
```
documents → split into chunks → embed → store in Chroma (vector DB)
question  → embed → similarity search → top-k chunks → LLM answers with that context
```

## Tech stack
**Python · LangChain · ChromaDB · OpenAI (embeddings + chat) · Gradio**

## Run it
```bash
cp .env.example .env         # set OPENAI_API_KEY
pip install -r requirements.txt
python ingest.py             # build the vector store
python app.py                # http://localhost:7860
```

---
<div align="center"><sub>Part of my AI/LLM engineering portfolio.</sub></div>
