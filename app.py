"""Gradio chat UI for the RAG Knowledge Worker.

Run locally:   python ingest.py   (once, to build the vector store)
               python app.py       (opens http://localhost:7860)
"""
import os

import gradio as gr
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set (add it to .env or as a Space secret).")

    from rag import KnowledgeWorker
    worker = KnowledgeWorker()

    def chat(message, history):
        answer, sources = worker.answer(message, history)
        if sources:
            answer += "\n\n---\n📚 *Sources: " + ", ".join(sources) + "*"
        return answer

    demo = gr.ChatInterface(
        chat,
        type="messages",
        title="🏦 Aurora Financial — Knowledge Worker",
        description="Ask about Aurora's products, security, pricing, or onboarding. "
                    "Answers are grounded in the company knowledge base (RAG).",
        examples=[
            "What certifications does Aurora have?",
            "How long does onboarding take?",
            "What products does Aurora offer?",
            "Is there a discount for startups?",
        ],
        theme=gr.themes.Soft(primary_hue="teal"),
    )
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")))


if __name__ == "__main__":
    main()
