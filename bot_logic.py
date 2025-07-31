import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()
# Fetching data from qdrant cloud
def load_vector_store():


    model_name = "BAAI/bge-large-en"
    embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": False}
    )
    
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    qdrant = QdrantVectorStore(
        client=client,
        collection_name="case_interview_prep_bot",
        embedding=embeddings
    )
    

    return qdrant

def create_conversational_rag_chain(vector_store):
    """
    Creates the main conversational RAG chain using Gemini.
    (This function remains unchanged)
    """
    # Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5 , api_key=os.getenv("GEMINI_API_KEY") )
    
    # The retriever component of the chain
    retriever = vector_store.as_retriever()

    # Prompt to rephrase a follow-up question
    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the conversation above, generate a search query to look up in order to get information relevant to the user's last question.")
    ])
    
    history_aware_retriever = create_history_aware_retriever(llm, retriever, retriever_prompt)

    # Prompt to answer the question based on context
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional case interview simulator. Your answers should be based on the context provided. Be concise and help the user practice their case-solving skills.\n\nContext:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    
    prompt_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    rag_chain = create_retrieval_chain(history_aware_retriever, prompt_chain)
    
    return rag_chain