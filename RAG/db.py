from sqlalchemy import create_engine,Column,Integer,String,Text,ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import SQLAlchemyError
DB_URL = "sqlite:///chat.db"
Base =  declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, nullable=False)
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    session = relationship("Session", back_populates="messages")

# Create the database and the tables
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to save a single message
def save_message(session_id: str, role: str, content: str):
    db = next(get_db())
    try:
        session = db.query(Session).filter(Session.session_id == session_id).first()
        if not session:
            session = Session(session_id=session_id)
            db.add(session)
            db.commit()
            db.refresh(session)

        db.add(Message(session_id=session.id, role=role, content=content))
        db.commit()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()

from langchain_core.messages import HumanMessage, AIMessage

def load_session_history(session_id: str) -> BaseChatMessageHistory:
    db = next(get_db())
    chat_history = ChatMessageHistory()
    try:
        session = db.query(Session).filter(Session.session_id == session_id).first()
        if session:
            for message in session.messages:
                if message.role == "user":
                    chat_history.add_message(HumanMessage(content=message.content))
                elif message.role == "assistant":
                    chat_history.add_message(AIMessage(content=message.content))
    except SQLAlchemyError:
        pass
    finally:
        db.close()
    
    return chat_history

# Modify the get_session_history function to use the database
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    
    if session_id not in store:
        store[session_id] = load_session_history(session_id)
    return store[session_id]

# Ensure you save the chat history to the database when needed
def save_all_sessions():
    for session_id, chat_history in store.items():
        for message in chat_history.messages:
            # Extract role and content from message objects
            role = "user" if message.type == "human" else "assistant"
            save_message(session_id, role, message.content)

# Example of saving all sessions before exiting the application
# import atexit
# atexit.register(save_all_sessions)
