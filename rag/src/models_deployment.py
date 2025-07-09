from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

# Load .env
env_path = Path.cwd().resolve() / '.env'
load_dotenv(dotenv_path=env_path)

cohere_api_key = os.getenv('COHERE_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

os.environ['COHERE_API_KEY'] = cohere_api_key
os.environ['GROQ_API_KEY'] = groq_api_key

client = Groq()

app = FastAPI()

# Enable CORS for your Angular dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a doctor, explain things thoroughly, try to analyze which illness could the patient suffer from and what's the best solution to resolve it."
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    reply = chat_completion.choices[0].message.content
    return {"reply": reply}
