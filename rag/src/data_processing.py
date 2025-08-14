from typing import Optional, List

import faiss
import cohere
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from .logger import get_logger

logger = get_logger(__name__)


class FilesDataProcessing:
    def __init__(self, query, docs = None):
        self.docs = docs
        self.query = query
    def embed_and_store(self):
        try:
            embeddings = CohereEmbeddings(model="embed-v4.0")
            index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
        except Exception as e:
            logger.error(f"Some error had occured during creation of embeddings object: {e}")
            return ["Error: failed to create embeddings"]

        vector_store = None
        try:
            vector_store = FAISS(
                embedding_function=embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                # It is in RAM, thus in future I will need to store it in Postgres container's volume
                index_to_docstore_id={},
            )
        except Exception as e:
            logger.error(f"Error during instantiation of the FAISS class's object: {e}")

        if self.docs:
            logger.info(f"Found {len(self.docs)} documents, proceeding to store them...")
            documents = [doc for doc in self.docs if doc is not None]
            ids = [f"{i}" for i in range(1, len(documents) + 1, 1)]
            vector_store.add_documents(documents=documents, ids=ids)
            results = vector_store.similarity_search_with_score(query=self.query, k=3)
            logger.info("Successfully added and selected 3 documents in the vector store.")
        else:
            logger.warning("There aren't any documents, living them as an empty list.")
            results = ["There aren't any documents!!!!"]
        return results

    def rerank(self, results) -> list:
        docs_content = [doc.page_content + " " + str(doc.metadata) for doc, score in results]

        try:
            co_rerank = cohere.ClientV2()
            response = co_rerank.rerank(
                model="rerank-v3.5",
                query=self.query,
                documents=docs_content,
                top_n=3,
            )

            reranked_docs = [docs_content[result.index] for result in response.results]

        except Exception as e:
            logger.error(f"Failed to rerank coherence: {e}")
            reranked_docs = docs_content

        return reranked_docs

    def preprocess(self) -> list:
        stored_embeddings = self.embed_and_store()
        return self.rerank(stored_embeddings)