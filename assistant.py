from typing import Optional
import streamlit as st
from phi.assistant import Assistant
from phi.knowledge import AssistantKnowledge
from phi.llm.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.embedder.openai import OpenAIEmbedder
from phi.embedder.ollama import OllamaEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.embedder.fireworks import FireworksEmbedder

groq_api_key = st.secrets["GROQ_API_KEY"]
exa_api_key = st.secrets["EXA_API_KEY"]

db_url = "postgresql://neondb_owner:gwiOVHQZ8qx1@ep-steep-cherry-a5tppkw8.us-east-2.aws.neon.tech/neondb?sslmode=require"
fireworks_api = "0IEJPt022AsY5IsP5t8Hb8TAy5OZXYTyEMQn3aRATAD2Sysh"


def get_auto_rag_assistant(
    llm_model: str = "llama3-70b-8192",
    embeddings_model: str = "text-embedding-3-small",
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Assistant:
    """Get a Groq Auto RAG Assistant."""

    # Define the embedder based on the embeddings model
    embedder = (
        OllamaEmbedder(model=embeddings_model, dimensions=768, api_key=groq_api_key)
        if embeddings_model == "nomic-embed-text"
        else OpenAIEmbedder(model=embeddings_model, dimensions=1536)
    )
    # Define the embeddings table based on the embeddings model
    embeddings_table = (
        "auto_rag_documents_groq_ollama"
        if embeddings_model == "nomic-embed-text"
        else "auto_rag_documents_groq_openai"
    )

    return Assistant(
        name="auto_rag_assistant_groq",
        run_id=run_id,
        user_id=user_id,
        llm=Groq(model=llm_model, api_key=groq_api_key, max_tokens=6000),
        storage=PgAssistantStorage(table_name="auto_rag_assistant_groq", db_url=db_url),
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=db_url,
                collection=embeddings_table,
                embedder=FireworksEmbedder(api_key=fireworks_api),
            ),
            # 3 references are added to the prompt
            num_documents=3,
        ),
        description="You are an Assistant called 'Chrisland Chatbot' that answers questions by calling functions.",
        instructions=[
            "First get additional information about the users question.",
            "You can use only the `search_knowledge_base` tool to search your knowledge base",
            # "If the user asks to summarize the conversation, use the `get_chat_history` tool to get your chat history with the user.",
            "Carefully process the information you have gathered and provide a clear and concise answer to the user.",
            "Respond directly to the user with your answer, do not say 'here is the answer' or 'this is the answer' or 'According to the information provided'",
            "NEVER mention your knowledge base or say 'According to the search_knowledge_base tool'",
        ],
        # Show tool calls in the chat
        show_tool_calls=False,
        # This setting gives the LLM a tool to search for information
        search_knowledge=True,
        # This setting gives the LLM a tool to get chat history
        read_chat_history=True,
        # tools=[DuckDuckGo()],
        # This setting tells the LLM to format messages in markdown
        markdown=True,
        # Adds chat history to messages
        add_chat_history_to_messages=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )
