import os
from typing import Optional, Tuple

from .logger import get_logger

from dotenv import load_dotenv, find_dotenv


logger = get_logger(__name__)
load_dotenv(find_dotenv(), override=True)

KEYS = ('COHERE_API_KEY', 'GROQ_API_KEY', 'LANGSMITH_API_KEY')


class ApiSetup:

    def __init__(self):

        logger.info("Api Setup START \n Deriving api keys from .env")

        self.set_api_key(KEYS)
        logger.info("Api keys loaded")

        self.set_langchain_api_settings()
        logger.info(f"Langchain api settings set")

    @staticmethod
    def set_api_key(environ_key_names: Tuple[str, ...]) -> None:
        for environ_key_name in environ_key_names:
            api_key = os.getenv(environ_key_name)
            if api_key is None:
                logger.error(f'{environ_key_name} environment variable not set')
                raise ValueError(f'{environ_key_name} not set in .env')
            os.environ['environ_key_name'] = api_key

    @staticmethod
    def set_langchain_api_settings() -> None:
        os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        os.environ['LANGCHAIN_PROJECT'] = 'RAG-Medical-Project'

    @staticmethod
    def get_django_key() -> Optional[str]:
        django_secret_key = os.getenv('DJANGO_SECRET_KEY')
        return django_secret_key


if __name__ == "__main__":
    api = ApiSetup()
    #print(api.cohere_api_key) Debug only with .self
