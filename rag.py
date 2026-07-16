"""The RAG core: retrieve relevant chunks, then answer grounded in them.

This is deliberately explicit (no hidden chain) so the flow is easy to follow:
  question -> embed -> similarity search -> stuff top-k chunks into the prompt ->
  LLM answers using only that context -> return answer + source filenames.
"""
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import config

load_dotenv(override=True)

SYSTEM_TEMPLATE = """You are a knowledge assistant for Aurora Financial.
Answer the user's question using ONLY the context below. If the answer is not in the
context, say you don't know — never invent facts, numbers, or policies.

Context:
{context}
"""


class KnowledgeWorker:
    def __init__(self):
        if not os.path.exists(config.VECTOR_STORE_DIR):
            raise FileNotFoundError(
                "Vector store not found. Build it first with:  python ingest.py"
            )
        embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.store = Chroma(
            persist_directory=config.VECTOR_STORE_DIR,
            collection_name=config.COLLECTION_NAME,
            embedding_function=embeddings,
        )
        self.retriever = self.store.as_retriever(search_kwargs={"k": config.RETRIEVER_K})
        self.llm = ChatOpenAI(model=config.CHAT_MODEL, temperature=0)

    @staticmethod
    def _format_context(docs):
        return "\n\n---\n\n".join(
            f"[source: {d.metadata.get('source', '?')}]\n{d.page_content}" for d in docs
        )

    @staticmethod
    def _to_lc_messages(history):
        """Convert Gradio 'messages' history into LangChain message objects."""
        out = []
        for turn in history or []:
            role, content = turn.get("role"), turn.get("content", "")
            out.append(HumanMessage(content) if role == "user" else AIMessage(content))
        return out

    def answer(self, question, history=None):
        """Return (answer_text, [source_filenames])."""
        docs = self.retriever.invoke(question)
        context = self._format_context(docs)

        messages = (
            [SystemMessage(SYSTEM_TEMPLATE.format(context=context))]
            + self._to_lc_messages(history)
            + [HumanMessage(question)]
        )
        response = self.llm.invoke(messages)
        sources = sorted({d.metadata.get("source", "?") for d in docs})
        return response.content, sources
