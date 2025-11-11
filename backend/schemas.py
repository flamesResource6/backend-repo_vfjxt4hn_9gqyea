from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Each Pydantic model corresponds to a MongoDB collection with the class name lowercased

class Knowledge(BaseModel):
    title: str
    description: Optional[str] = None
    tags: List[str] = []
    source_url: Optional[str] = None

class Prompt(BaseModel):
    name: str
    content: str
    variables: List[str] = []

class Document(BaseModel):
    title: str
    content: str
    type: str = Field(default="text")

class ChatbotShape(BaseModel):
    name: str
    primary_color: str = "#ff7a00"
    accent_color: str = "#111827"
    bubble_style: str = "rounded"
    avatar: Optional[str] = None

class Plan(BaseModel):
    tier: str
    seats: int = 1
    monthly_price: float

class APIKey(BaseModel):
    name: str
    key: str
    scopes: List[str] = ["read", "write"]

# Simple Chat message model for demo chat UI
class ChatMessage(BaseModel):
    role: str
    content: str
