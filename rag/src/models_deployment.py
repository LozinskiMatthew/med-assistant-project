from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import jwt
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
from .logger import get_logger
from langchain_community.document_loaders import PyPDFLoader

logger = get_logger(__name__)

# Load .env
env_path = Path.cwd().resolve() / '.env'
load_dotenv(dotenv_path=env_path)

cohere_api_key = os.getenv('COHERE_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
django_secret_key = os.getenv('DJANGO_SECRET_KEY')

# Log environment setup
logger.info("=== FastAPI Starting ===")
logger.info(f"COHERE_API_KEY exists: {bool(cohere_api_key)}")
logger.info(f"GROQ_API_KEY exists: {bool(groq_api_key)}")
logger.info(f"DJANGO_SECRET_KEY exists: {bool(django_secret_key)}")
if django_secret_key:
    logger.info(f"DJANGO_SECRET_KEY first 10 chars: {django_secret_key[:10]}...")

os.environ['COHERE_API_KEY'] = cohere_api_key
os.environ['GROQ_API_KEY'] = groq_api_key

client = Groq()
app = FastAPI()

# Security scheme
security = HTTPBearer()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    logger.info("=== Authentication Debug ===")

    try:
        token = credentials.credentials
        logger.info(f"Received token length: {len(token)}")
        logger.info(f"Token first 20 chars: {token[:20]}...")
        logger.info(f"Token last 20 chars: ...{token[-20:]}")

        if not django_secret_key:
            logger.error("DJANGO_SECRET_KEY is None or empty!")
            raise HTTPException(status_code=500, detail="Server configuration error")

        logger.info("Attempting to decode JWT...")
        payload = jwt.decode(token, django_secret_key, algorithms=["HS256"])
        logger.info(f"Successfully decoded JWT. Payload keys: {list(payload.keys())}")
        logger.info(f"Full payload: {payload}")

        user_id = payload.get("user_id")
        logger.info(f"Extracted user_id: {user_id} (type: {type(user_id)})")

        if user_id is None:
            logger.error("user_id is None in JWT payload")
            raise HTTPException(status_code=401, detail="Invalid token - no user_id")

        logger.info(f"Authentication successful for user_id: {user_id}")
        return user_id

    except jwt.ExpiredSignatureError as e:
        logger.error(f"JWT Expired: {e}")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.DecodeError as e:
        logger.error(f"JWT Decode Error: {e}")
        raise HTTPException(status_code=401, detail="Token decode error")
    except jwt.InvalidTokenError as e:
        logger.error(f"JWT Invalid Token Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail="Authentication error")


def get_user_documents_path(user_id: int) -> Path:
    documents_base = Path("/app/shared_documents")
    user_path = documents_base / f"user_{user_id}"
    logger.info(f"User documents path: {user_path}")
    return user_path


def load_user_documents(user_id: int) -> str:
    """Load and process user's documents for RAG"""
    logger.info(f"=== Document Loading Debug for user_{user_id} ===")

    user_docs_path = get_user_documents_path(user_id)
    logger.info(f"Looking for documents in: {user_docs_path}")
    logger.info(f"Path exists: {user_docs_path.exists()}")

    if not user_docs_path.exists():
        logger.warning(f"User documents directory does not exist: {user_docs_path}")
        return "No documents found for this user."

    # List all files in directory
    try:
        all_files = list(user_docs_path.glob("*"))
        logger.info(f"Files found in directory: {[f.name for f in all_files]}")
    except Exception as e:
        logger.error(f"Error listing files in {user_docs_path}: {e}")
        return "Error accessing user documents."

    documents_content = []

    for doc_file in user_docs_path.glob("*"):
        logger.info(
            f"Processing file: {doc_file.name} (size: {doc_file.stat().st_size if doc_file.exists() else 'N/A'})")

        if doc_file.is_file():
            logger.info(f"File extension: {doc_file.suffix.lower()}")

            if doc_file.suffix.lower() in ['.pdf']:
                try:
                    logger.warning(f"Attempting to read PDF as text: {doc_file.name}")
                    loader = []
                    loader = PyPDFLoader(os.path.join(user_docs_path, doc_file.name))
                    pages = loader.load()
                    logger.info(f"Successfully read {doc_file.name}, pages length: {len(pages)}")
                    documents_content.append("\n".join(pages[page].page_content for page in range(len(pages))))
                except Exception as e:
                    logger.error(f"Error reading {doc_file}: {type(e).__name__}: {e}")
            else:
                logger.info(f"Skipping file {doc_file.name} - not a supported format")

    if documents_content:
        result = "\n\n\n\n\n\n".join(
            f"\n\n\n Document {i}\n\n\n{doc}" for i, doc in enumerate(documents_content)
        )
    else:
        result = "No readable documents found."
    logger.info(f"Final documents content length: {len(result)}")
    return result[:2500]


@app.post("/chat")
async def chat(request: ChatRequest, current_user: int = Depends(get_current_user)):
    logger.info(f"=== Chat Request from user_{current_user} ===")
    logger.info(f"User message: {request.message[:100]}..." if len(
        request.message) > 100 else f"User message: {request.message}")

    try:
        # Load user's documents for context
        user_documents = load_user_documents(current_user)
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