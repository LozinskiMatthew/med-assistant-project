import os
import re
from typing import Annotated, List, Literal, Optional
from typing_extensions import TypedDict

import cohere
import faiss
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.documents.base import Document
from langchain_community.document_loaders import WebBaseLoader

from .logger import get_logger

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "RAG-Medical-Project"

llm_rewriter = ChatGroq(temperature=0.01, model="llama-3.1-8b-instant")
llm_answerer = ChatGroq(temperature=0.5, model="deepseek-r1-distill-llama-70b")

rewrites_redirection = None


# Define the state with message history
class State(TypedDict, total=False):
    messages: Annotated[List, add_messages]
    rewritten_query: Optional[str]
    retrieved_docs: List[str]
    retrieved_webpage_docs: List[str]
    reflection_count: int
    router_decision: Optional[Literal["scrape_webpages", "self_reflect", "answerer", "rewriter", "retriever"]]
    user_prompt: Optional[str]
    scraped_count: int
    input_docs: List[Document]
    last_reflection: Optional[str]
    rewrites_redirection: bool


logger = get_logger()
logger.info("It's me")

medical_sites = [
    {
        "name": "Mayo Clinic",
        "url": "https://www.mayoclinic.org",
        "description": "Trusted medical information from a world-renowned clinical and research institution. Offers detailed content on diseases, conditions, tests, and procedures."
    },
    {
        "name": "WebMD",
        "url": "https://www.webmd.com",
        "description": "Popular consumer health site featuring a symptom checker, drug info, and doctor-reviewed health articles written in layman's terms."
    }
]

class RAG:

    def __init__(self, med_sites):
        self.med_sites = med_sites
        self.graph_running = False


    def rewriter(self, state: State) -> State:
        """Rewrite user message to be keyword-friendly for vector search"""
        # Get the last user message - fixed to access content attribute

        global rewrites_redirection

        logger.info("REWRITER!!!")
        logger.info("I am being launched")
        logger.info(f"I see: state[rewrites_redirection] as {state['rewrites_redirection']}")

        logger.info(f"Here is the value of, rewrites_redirection global variable: {rewrites_redirection} (1)")

        human_message = state["user_prompt"]

        messages = [
            SystemMessage(
                content="You are a helpful assistant that rewrites verbose user questions into short, keyword-rich queries suitable for vector similarity search. Do not answer the question. Only return the rewritten query.\n\nExample:\nInput: 'Can you explain what the difference is between SQL and NoSQL databases and when to use them?'\nOutput: 'difference SQL vs NoSQL databases usage scenario'\n"),
            HumanMessage(content=human_message),
        ]

        # Your LLM call to rewrite the query
        rewritten = llm_rewriter.invoke(messages)

        logger.info(f"Here is the value of, rewrites_redirection global variable: {rewrites_redirection} (2)")

        return {
            "messages": [SystemMessage(content=f"Query rewritten to: {rewritten.content}")],
            "rewritten_query": rewritten.content,
            "rewrites_redirection": rewrites_redirection
        }


    def retriever(self, state: State) -> State:
        """Retrieve documents based on rewritten query"""

        logger.info("RETRIVER!!!")
        logger.info("I am being launched")

        query = state["rewritten_query"]
        embeddings = CohereEmbeddings(model="embed-v4.0")
        index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

        vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            # It is in RAM, thus in future I will need to store it in Postgres container's volume
            index_to_docstore_id={},
        )
        docs = state["input_docs"]
        # Add documents to the vector store - only if docs exist
        if docs:
            documents = [doc for doc in docs if doc is not None]
            ids = [f"{i}" for i in range(1, len(documents) + 1, 1)]
            vector_store.add_documents(documents=documents, ids=ids)
            results = vector_store.similarity_search_with_score(query=query, k=3)

            co_rerank = cohere.ClientV2()

            docs_content = [doc.page_content + " " + str(doc.metadata) for doc, score in results]

            response = co_rerank.rerank(
                model="rerank-v3.5",
                query=query,
                documents=docs_content,
                top_n=3,
            )

            reranked_docs = [docs_content[result.index] for result in response.results]
        else:
            reranked_docs = []

        scraped_count = state.get("scraped_count", 0)

        return {
            "messages": [SystemMessage(content=f"Retrieved {len(reranked_docs)} documents")],
            "retrieved_docs": reranked_docs,
            "scraped_count": scraped_count
        }


    def router(self, state: State) -> State:
        """Decide whether to scrape web, self-reflect, or respond to user"""

        logger.info("ROUTER!!!")
        logger.info("I am being launched")

        if state["user_prompt"] is None:
            human_message = state["messages"][-1].content
        else:
            human_message = state["user_prompt"]

        reflection_count = state.get("reflection_count", 0)
        retrieved_docs = state.get("retrieved_docs", [])
        scraped_count = state.get("scraped_count", 0)

        retrieved_doc_info = f" retrieved documents: {retrieved_docs}" if retrieved_docs else ""
        retrieved_webpages_info = f", on the retrieved medical websites content: {retrieved_docs}" if retrieved_docs else ""

        prompt = f"""
        Your task is to route to the other option, writing simply one word.
        Based on the:
        {retrieved_doc_info}
        {retrieved_webpages_info}
        , reflection count: {reflection_count}
        , and scraped count: {scraped_count}
    
        Should I:
        1. "scrape_webpages" - if scraped webpages's docs are insufficient (or scrape count is greater than 3), but you must DO THIS at least once!
        2. "retrieve_docs" - if retrieved docs are insufficient (or scrape count is greater than 3), but you must DO THIS at least once!
        3. "self_reflect" - if I need to analyze more (can do it only if reflection count is lesser than 3)
        4. "answerer" - if I'm ready to respond (or scrape count is greater than 3)
    
        Remember you MUST return only one of these four words: retrieve_docs, scrape_webpages, self_reflect, or answerer.
        """
        llm_decision = llm_answerer.invoke([SystemMessage(content=prompt), HumanMessage(
            content="Respond with only one word, out of these three words: retrieve_docs, scrape_webpages, self_reflect, or answerer.")]).content.strip()
        words = ("router_decision", "answerer", "retrieve_docs", "scrape_webpages", "self_reflect")
        pattern = r"(" + "|".join(words) + r")(?=[^a-zA-Z_]|$)"

        logger.info(f"I am a router node and this is llm_decision: {llm_decision}")
        matches = list(re.finditer(pattern, llm_decision))

        solution = matches[-1].group(1) if matches else "answerer"

        return {
            "messages": [SystemMessage(content=f"Router decision: {solution}")],
            "router_decision": solution,
            "user_prompt": human_message,
        }

    def scrape_webpages(self, state: State) -> State:
        """Scrape web pages for additional information"""
        # Soon I should add a model to check which sites to visit.

        logger.info("SCRAPER OF THE WEBSITES!!!")
        logger.info("I am being launched")

        try:
            loader = WebBaseLoader([site["url"] for site in self.med_sites])
            docs_scraped = loader.load()

            if docs_scraped:
                scraped_content = f"Scraped content from the chosen websites, with their titles related to {state['rewritten_query']}, is as follows: '<Document name={docs_scraped[0].metadata.get('title', '')}>\n{docs_scraped[0].page_content}\n</Document>'"
            else:
                scraped_content = "No content was scraped from the websites."
        except Exception as e:
            scraped_content = f"Error scraping websites: {str(e)}"

        # Add scraped content to retrieved docs
        updated_docs = state["retrieved_webpage_docs"] + [scraped_content]
        scraped_count = state.get("scraped_count", 0) + 1

        return {
            "messages": [SystemMessage(content="Web scraping completed, retrieved docs")],
            "retrieved_webpage_docs": updated_docs,
            "scraped_count": scraped_count
        }


    def self_reflect(state: State) -> State:
        logger.info("SELF REFLECT!!!")
        logger.info("I am being launched")

        reflection_count = state.get("reflection_count", 0) + 1
        last_reflection = f", and on your last reflection: {state['last_reflection']}" if state[
                                                                                              'last_reflection'] is not None else ""
        reflection = llm_answerer.invoke([HumanMessage(
            content=f"Analyze this, and reflect on the following:, the prompt from a user: {state['user_prompt']}, and on the documents {state['retrieved_docs']} and/or medical websites content that were previously retrieved: {state['retrieved_webpage_docs']}{last_reflection}")])

        return {
            "messages": [AIMessage(content=reflection.content)],
            "reflection_count": reflection_count,
            "last_reflection": reflection
        }


    def answerer(self, state: State) -> State:
        """Generate final response to user"""

        logger.info("ANSWERER!!!")
        logger.info("I am being launched")

        answer = llm_answerer.invoke([HumanMessage(
            content=f"Answer based on retrieved documents: {state['retrieved_docs']}, documents scraped from the websites; {state['retrieved_webpage_docs']} on your previous self reflection on the user question: {state['last_reflection']} and on the initial user prompt {state['user_prompt']}")])  # Also on it's last reflection

        return {
            "messages": [AIMessage(content=answer.content)]
        }


    def route_decision(self, state: State) -> Literal["scrape_webpages", "self_reflect", "answerer", "rewriter", "retriever"]:
        logger.info("ROUTE DECISION NODE LAUNCHED!!!")
        logger.info("I am being launched")

        decision = state.get("router_decision", "answerer")
        valid_routes = {"scrape_webpages", "rewriter", "retriever", "self_reflect", "answerer"}
        if decision not in valid_routes:
            logger.error(f"Invalid decision from router: {decision}")
        if decision in ("scrape_webpages", "retrieve_docs"):
            logger.info("I am in decision in (scrape_webpage, retrieve_docs) condition")
            if state["rewritten_query"] is None:
                global rewrites_redirection
                if decision == "retrieve_docs":
                    rewrites_redirection = True
                else:
                    rewrites_redirection = False
                logger.info(f"Here is the value of, rewrites_redirection global variable: {rewrites_redirection}")
                return "rewriter"

        if decision == "scrape_webpages":
            return "scrape_webpages"
        elif decision == "self_reflect":
            return "self_reflect"
        elif decision == "retrieve_docs":
            return "retriever"
        else:
            logger.info("I am defaulting to answerer")
            logger.info("I am defaulting to answerer")
            logger.info(f"This is routers decision {state.get('router_decision', 'answerer')}")
            return "answerer"


    # Create the graph
    def create_rag_graph(self):
        rag = StateGraph(State)

        rag.add_node("router", self.router)
        rag.add_node("rewriter", self.rewriter)
        rag.add_node("retriever", self.retriever)
        rag.add_node("scrape_webpages", self.scrape_webpages)
        rag.add_node("self_reflect", self.self_reflect)
        rag.add_node("answerer", self.answerer)

        # Add edges
        rag.add_edge(START, "router")

        # Conditional edges from router
        rag.add_conditional_edges(
            "router",
            self.route_decision,
            {
                "scrape_webpages": "scrape_webpages",
                "rewriter": "rewriter",
                "retriever": "retriever",
                "self_reflect": "self_reflect",
                "answerer": "answerer"
            }
        )

        rag.add_conditional_edges(
            "rewriter",
            lambda state: state["rewrites_redirection"],
            {
                True: "retriever",
                False: "scrape_webpages"
            }
        )

        rag.add_edge("scrape_webpages", "router")

        rag.add_edge("self_reflect", "router")

        rag.add_edge("retriever", "router")

        rag.add_edge("answerer", END)

        self.graph_running = True

        return rag.compile()


    def run(self, human_message, docs):
        if self.graph_running == False:
            rag_graph = self.create_rag_graph()

        initial_state = {
            "messages": [HumanMessage(content=human_message)],
            "rewritten_query": None,
            "user_prompt": None,
            "retrieved_docs": [],
            "retrieved_webpage_docs": [],
            "reflection_count": 0,
            "scraped_count": 0,
            "router_decision": None,
            "input_docs": docs,
            "last_reflection": None,
            "rewrites_redirection": None
        }

        final_state = rag_graph.invoke(initial_state)
        logger.info(f"\n\n\n Final_state from deployment model: \n  {final_state} \n\n\n")
        print("Final message:", final_state["messages"][-1])
        return final_state["messages"][-1]


def split_text(self, user_id):
    # Get users id
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

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('/app/shared_documents/user_1/Lab0_Laravel11.pdf')
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1800,
    chunk_overlap=300,
    length_function=len,
    separators=["\n\n", "\n", " ", ""],
    is_separator_regex=False
)

docs = text_splitter.split_documents(pages)

print(docs[7])

if __name__ == "main":

    rag = RAG(medical_sites)

    rag_graph = rag.create_rag_graph()

    initial_state = {
        "messages": [HumanMessage(content="I am kinda sick, my headache, I would like to search web for it...")],
        "rewritten_query": None,
        "user_prompt": None,
        "retrieved_docs": [],
        "retrieved_webpage_docs": [],
        "reflection_count": 0,
        "scraped_count": 0,
        "router_decision": None,
        "input_docs": docs,
        "last_reflection": None,
        "rewrites_redirection": None
    }

    # Run the graph
    final_state = rag_graph.invoke(initial_state)
    logger.info(f"\n\n\n Final_state from deployment model: \n  {final_state} \n\n\n")
    print("Final messages:", final_state["messages"])
