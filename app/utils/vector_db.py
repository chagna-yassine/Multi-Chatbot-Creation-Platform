from chromadb.config import Settings
import chromadb

# Initialize Chroma client with the correct implementation
chroma_client = chromadb.Client()

# Initialize collection for storing chatbot embeddings
def get_or_create_collection(chatbot_id: str):
    collection_name = f"chatbot_{chatbot_id}"
    
    # Check if the collection already exists
    existing_collections = [col.name for col in chroma_client.list_collections()]
    if collection_name in existing_collections:
        return chroma_client.get_collection(name=collection_name)
    
    # Create a new collection if it doesn't exist
    return chroma_client.create_collection(name=collection_name)

def store_embeddings(chatbot_id: str, embeddings, sentences):
    collection = get_or_create_collection(chatbot_id)
    
    # print(f"Storing embeddings for chatbot {chatbot_id}")  # Debug
    
    for idx, (embedding, sentence) in enumerate(zip(embeddings, sentences)):
        # print(f"Adding embedding for sentence: {sentence}")  # Debug
        
        collection.add(
            ids=[f"{chatbot_id}_{idx}"],
            embeddings=[embedding.tolist()],
            documents=[sentence],  # Store sentence as document
            metadatas=[{"sentence": sentence}]
        )
    
    return {"message": "Embeddings stored successfully"}

