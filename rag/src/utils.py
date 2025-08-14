import os.path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def split_text(self, user_id):
    folder = f"/app/shared_documents/{user_id}"
    pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    all_pages = []

    for file in pdf_files:
        path = os.path.join(folder, file)
        loader = PyPDFLoader(path)
        pages = loader.load()
        all_pages.append(pages)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1800,
        chunk_overlap=300,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
        is_separator_regex=False
    )

    splitted_docs = []
    for page in all_pages:
        splitted_docs.append(text_splitter.split_documents(page))
    return splitted_docs

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