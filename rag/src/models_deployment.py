from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

from . import api_setup
from . import data_ingestion
from .logger import get_logger

logger = get_logger(__name__)

api_setup = api_setup.ApiSetup()
django_secret_key = api_setup.get_django_secret_key()

client = Groq()
app = FastAPI()

ingestion = data_ingestion.DataIngestion(django_secret_key, client, app)

class ChatRequest(BaseModel):
    message: str

from . import model_deployment

# request.message -> user message
@app.post("/chat")
async def chat(request: ChatRequest, current_user: int = ingestion.get_current_user):
    logger.info(f"=== Chat Request from user_{current_user} ===")
    logger.info(f"User message: {request.message[:100]}..." if len(
        request.message) > 100 else f"User message: {request.message}")

    try:
        # Load user's documents for context
        user_documents = ingestion.load_user_documents(current_user)
        # user_documents -> string
        logger.info(f"User documents loaded, length: {len(user_documents)}")

        # Create system prompt with user's documents
        system_prompt = f"""Your task is to make a concise description of user documents:

User's Documents:
{user_documents}
"""

        logger.info("Sending request to Groq...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        reply = chat_completion.choices[0].message.content
        logger.info(f"Groq response length: {len(reply)}")
        logger.info("Chat request completed successfully")

        return {"reply": reply, "user_id": current_user}

    except Exception as e:
        logger.error(f"Error in chat endpoint: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")