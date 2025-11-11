from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel
import os

from database import create_document, get_documents
from schemas import Knowledge, Prompt, Document, ChatbotShape, Plan, APIKey, ChatMessage

app = FastAPI(title="Chatbot Dashboard API", version="1.0.0")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend running", "version": "1.0.0"}

@app.get("/test")
async def test_db():
    # Probe DB connection and list collections
    from database import get_db
    db = await get_db()
    collections = await db.list_collection_names()
    return {
        "backend": "ok",
        "database": "mongo",
        "database_url": os.getenv("DATABASE_URL", "mongodb://localhost:27017"),
        "database_name": os.getenv("DATABASE_NAME", "vibe_db"),
        "connection_status": "connected",
        "collections": collections,
    }

# CRUD-lite endpoints for panels

@app.post("/knowledge", response_model=Dict[str, Any])
async def create_knowledge(item: Knowledge):
    return await create_document("knowledge", item.model_dump())

@app.get("/knowledge", response_model=List[Dict[str, Any]])
async def list_knowledge():
    return await get_documents("knowledge")

@app.post("/prompts", response_model=Dict[str, Any])
async def create_prompt(item: Prompt):
    return await create_document("prompt", item.model_dump())

@app.get("/prompts", response_model=List[Dict[str, Any]])
async def list_prompts():
    return await get_documents("prompt")

@app.post("/documents", response_model=Dict[str, Any])
async def create_doc(item: Document):
    return await create_document("document", item.model_dump())

@app.get("/documents", response_model=List[Dict[str, Any]])
async def list_docs():
    return await get_documents("document")

@app.post("/chatbot-shape", response_model=Dict[str, Any])
async def create_shape(item: ChatbotShape):
    return await create_document("chatbotshape", item.model_dump())

@app.get("/chatbot-shape", response_model=List[Dict[str, Any]])
async def list_shapes():
    return await get_documents("chatbotshape")

@app.post("/plan", response_model=Dict[str, Any])
async def create_plan(item: Plan):
    return await create_document("plan", item.model_dump())

@app.get("/plan", response_model=List[Dict[str, Any]])
async def list_plans():
    return await get_documents("plan")

@app.post("/api-keys", response_model=Dict[str, Any])
async def create_api_key(item: APIKey):
    return await create_document("apikey", item.model_dump())

@app.get("/api-keys", response_model=List[Dict[str, Any]])
async def list_api_keys():
    return await get_documents("apikey")

# Simple mock chat response (no external LLM)
class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/chat", response_model=Dict[str, Any])
async def chat(req: ChatRequest):
    # Echo-style simple bot that replies with a friendly message
    last_user = next((m for m in reversed(req.messages) if m.role == "user"), None)
    reply = "Hello! How can I assist you today?"
    if last_user:
        reply = f"You said: '{last_user.content}'. I'm a demo bot in this dashboard."
    return {"reply": reply}
