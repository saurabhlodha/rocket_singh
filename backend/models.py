from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="active")  # active, completed, abandoned
    messages = relationship("Message", back_populates="conversation")
    order = relationship("Order", back_populates="conversation", uselist=False)
    
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text)
    role = Column(String)  # user or assistant
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")

class SystemPrompt(Base):
    __tablename__ = "system_prompt"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # system_prompt, conversation_flow
    content = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    customer_name = Column(String)
    customer_email = Column(String)
    customer_address = Column(String)
    order_type = Column(String)  # wood or wood-aluminium
    specifications = Column(JSON)  # Store all order specifications
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, quoted, confirmed, cancelled
    conversation = relationship("Conversation", back_populates="order")
