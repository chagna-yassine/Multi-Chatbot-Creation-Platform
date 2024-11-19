from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Chatbot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    tone = Column(String, nullable=True)  # Personality tone
    behavior = Column(String, nullable=True)  # Personality behavior
    created_at = Column(DateTime, default=datetime.utcnow)

    # Foreign key linking to the user who created the chatbot
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chatbots")
