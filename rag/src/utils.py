import os.path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def prepare_docs(user, path, cs=1800, co=300) -> List[Document]: # In future I can make it so it will do paths in for loop
    docs_path = os.path.join("/app/shared_documents", f"user_{user}", path)
    loader = PyPDFLoader(docs_path)
    pages = loader.load()

    # Initialize the splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cs,  # max characters per chunk
        chunk_overlap=co,  # overlap between chunks
        length_function=len,  # use character count
        separators=["\n\n", "\n", " ", ""],  # split hierarchy
        is_separator_regex=False
    )
    return text_splitter.split_documents(pages)

MEDICAL_SITES = [
    {
        "name": "Matthew Clinic",
        "url": "https://www.matthewlozinski.com/",
        "description": "Trusted medical researcher from a world-renowned clinical and research institution. Offers detailed content on diseases, conditions, tests, and procedures."
    },
    {
        "name": "Mayo Clinic",
        "url": "https://www.mayoclinic.org",
        "description": "Trusted medical information from a world-renowned clinical and research institution. Offers detailed content on diseases, conditions, tests, and procedures."
    },
    {
        "name": "WebMD",
        "url": "https://www.webmd.com",
        "description": "Popular consumer health site featuring a symptom checker, drug info, and doctor-reviewed health articles written in layman's terms."
    },
    {
        "name": "MedlinePlus",
        "url": "https://medlineplus.gov",
        "description": "A service of the U.S. National Library of Medicine providing free, reliable health information in multiple languages with no ads or commercial bias."
    },
    {
        "name": "Healthline",
        "url": "https://www.healthline.com",
        "description": "Health and wellness site with medical articles reviewed by experts, covering fitness, nutrition, mental health, and medical conditions."
    },
    {
        "name": "BMJ (British Medical Journal)",
        "url": "https://www.bmj.com",
        "description": "Leading peer-reviewed journal providing clinical research, reviews, medical news, and opinion pieces for healthcare professionals."
    }
]