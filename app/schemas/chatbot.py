from pydantic import BaseModel
from typing import Optional

class ChatbotCreate(BaseModel):
    name: str
    description: str
    tone: Optional[str] = None  
    behavior: Optional[str] = None  

class ChatbotOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    tone: Optional[str] = None
    behavior: Optional[str] = None

    class Config:
        from_attributes = True

class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tone: Optional[str] = None
    behavior: Optional[str] = None

class QueryRequest(BaseModel):
    query: str