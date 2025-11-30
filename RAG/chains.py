import sys
import os

# Add RAG directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

# Import dependencies from other modules
from helpers import vectorstore, get_chat_model, format_docs
from prompts import system_prompt
from db import get_session_history
from preprocess import initialise_embed

# Initialize components
embedding_function = initialise_embed()
retriever = vectorstore(embedding_function)
llm = get_chat_model()

rag_chain = (
    {"context":itemgetter("question")|retriever | format_docs,
     "question":RunnablePassthrough(),
     "chat_history":itemgetter("chat_history")}
    | system_prompt
    | llm
    | StrOutputParser()
)


chain_with_message_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)
