from database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, Text, JSON
from sqlalchemy.orm import Relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String)
    content = Column(Text)
    memory = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

