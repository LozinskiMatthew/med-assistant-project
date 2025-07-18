import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from rag.src.logger import get_logger

logger = get_logger(__name__)

env_path = Path.cwd().resolve().parents[1] / '.env'

load_dotenv(find_dotenv(), override=True)

class ApiSetup:
    def __init__(self):

        logger.info("Api Setup START \n Deriving api keys from .env")

        cohere_api_key = os.getenv('COHERE_API_KEY')
        if cohere_api_key is None:
            logger.error('COHERE_API_KEY environment variable not set')
            raise ValueError("COHERE_API_KEY not set in .env")


        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key is None:
            logger.error("GROQ_API_KEY not set in .env")
            raise ValueError("GROQ_API_KEY not set in .env")

        langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
        if langsmith_api_key is None:
            logger.error("LANGSMITH_API_KEY not set in .env")
            raise ValueError("LANGSMITH_API_KEY not set in .env")

        logger.info("Api keys successfully loaded")

        logger.info(f"Setting the env variables to langsmith, cohere and api keys.")

        os.environ['COHERE_API_KEY'] = cohere_api_key
        os.environ['GROQ_API_KEY'] = groq_api_key
        os.environ['LANGSMITH_API_KEY'] = langsmith_api_key

if __name__ == "__main__":
    api = ApiSetup()
    #print(api.cohere_api_key) Debug only with .self