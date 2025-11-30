from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

system_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an intelligent AI assistant use the following context to answer the question:\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("user", "{question}")
])

