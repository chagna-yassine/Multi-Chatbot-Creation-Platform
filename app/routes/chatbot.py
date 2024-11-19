from app.schemas.chatbot import ChatbotCreate, ChatbotOut, ChatbotUpdate, QueryRequest
from app.utils.file_handler import save_file, extract_text, generate_embeddings
from app.utils.vector_db import store_embeddings, get_or_create_collection
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from app.utils.dependencies import get_current_user
# from app.utils.ai_model import generate_response
from app.models.chatbot import Chatbot
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# Endpoint: Create a chatbot
@router.post("/", response_model=ChatbotOut)
def create_chatbot(
    chatbot: ChatbotCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Create new chatbot
    new_chatbot = Chatbot(
        name=chatbot.name,
        description=chatbot.description,
        tone=chatbot.tone,
        behavior=chatbot.behavior,
        user_id=user.id
    )
    db.add(new_chatbot)
    db.commit()
    db.refresh(new_chatbot)
    return new_chatbot

@router.patch("/{chatbot_id}", response_model=ChatbotOut)
def update_chatbot(
    chatbot_id: int,
    chatbot_update: ChatbotUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Retrieve the chatbot
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id, Chatbot.user_id == user.id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    # Update fields dynamically
    if chatbot_update.name:
        chatbot.name = chatbot_update.name
    if chatbot_update.description:
        chatbot.description = chatbot_update.description
    if chatbot_update.tone:
        chatbot.tone = chatbot_update.tone
    if chatbot_update.behavior:
        chatbot.behavior = chatbot_update.behavior

    # Commit changes
    db.commit()
    db.refresh(chatbot)
    return chatbot

@router.get("/{chatbot_id}", response_model=ChatbotOut)
def get_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id, Chatbot.user_id == user.id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return chatbot

@router.post("/{chatbot_id}/upload")
def upload_knowledge_base(
    chatbot_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check if chatbot exists and belongs to the user
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id, Chatbot.user_id == user.id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    # Save and process the file
    file_path = save_file(file)
    text = extract_text(file_path)
    embeddings, sentences = generate_embeddings(text)

    # Store embeddings in the vector database
    result = store_embeddings(chatbot_id=str(chatbot_id), embeddings=embeddings, sentences=sentences)

    return {
        "message": "File processed and embeddings stored successfully",
        "result": result
    }

@router.post("/{chatbot_id}/query")
def query_knowledge_base(
    chatbot_id: int,
    query_request: QueryRequest,  # Use the Pydantic schema
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Extract the query from the request body
    query = query_request.query

    # Retrieve the collection for the chatbot
    collection = get_or_create_collection(chatbot_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Knowledge base not found")

    # Perform similarity search
    results = collection.query(
        query_texts=[query],
        n_results=5  # Number of results to return
    )

    return {"query": query, "results": results}

@router.get("/{chatbot_id}/collection")
def list_collection_data(
    chatbot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    collection = get_or_create_collection(chatbot_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Retrieve all data in the collection
    data = collection.get()
    return {"collection_name": collection.name, "data": data}

# @router.post("/{chatbot_id}/respond")
# def ai_powered_response(
#     chatbot_id: int,
#     query_request: QueryRequest,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user)
# ):
#     # Fetch context snippets
#     collection = get_or_create_collection(chatbot_id)
#     if not collection:
#         raise HTTPException(status_code=404, detail="Knowledge base not found")
    
#     results = collection.query(
#         query_texts=[query_request.query],
#         n_results=3,
#         include=["documents"]
#     )
#     context_snippets = results["documents"][0] if results["documents"] else []

#     # Prepare prompt
#     context = "\n".join(context_snippets)
#     prompt = f"Context:\n{context}\n\nQuery: {query_request.query}\n\nResponse:"
    
#     # Generate response
#     response = generate_response(prompt)
    
#     return {"query": query_request.query, "response": response, "context": context_snippets}
