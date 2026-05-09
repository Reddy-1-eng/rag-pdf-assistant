# RAG (Retrieval-Augmented Generation) module

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Use the correct working models from API test
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Use absolute path for database
DB_PATH = os.path.join(SCRIPT_DIR, "vector_db")

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = pdf_path

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_documents(docs)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    return f"{len(chunks)} chunks stored successfully."


def ask_question(question):
    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    sources = [
        {
            "page": doc.metadata.get("page"),
            "source": doc.metadata.get("source")
        }
        for doc in docs
    ]

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI PDF assistant.

Answer ONLY from the provided context.

If answer is not present in context,
say:
"I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return {
        "answer": response,
        "sources": sources
    }