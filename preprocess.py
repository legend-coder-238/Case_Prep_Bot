from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean
from unstructured.chunking.title import chunk_by_title
from unstructured.documents.elements import ElementMetadata
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

load_dotenv()

pdf_path = r"E:\...\Casebooks\..."
elements = partition_pdf(pdf_path, strategy="fast", chunking_strategy="by_title")
print(f"Partition complete: {len(elements)} elements found")

print("Cleaning elements...")
cleaned_elements = []
for i, element in enumerate(elements):
    cleaned_text = clean(
        element.text,
        bullets=True,
        extra_whitespace=True,
        dashes=True,
        lowercase=False,
        trailing_punctuation=True
    )

    element.text = cleaned_text
    cleaned_elements.append(element)
print("Cleaning complete")

chunks = chunk_by_title(cleaned_elements)
print("Chunking complete")
print(f"Total chunks created: {len(chunks)}")


model_name = "BAAI/bge-large-en"
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": False}
)
langchain_docs = [
    Document(page_content=chunk.text, metadata=chunk.metadata.to_dict())
    for chunk in chunks
]

qdrant = Qdrant.from_documents(
    langchain_docs,
    embeddings,
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    prefer_grpc=True,
    collection_name="casebook_vector_db"
)
print("Data pushed to Qdrant Cloud.")

# Count vectors in DB 
client = QdrantClient(
    url="https://93375cc8-fbb5-4562-bd92-b5a896439091.us-east4-0.gcp.cloud.qdrant.io",
    api_key=os.getenv("QDRANT_API_KEY"),
)
count = client.count("casebook_vector_db", exact=True).count
print(f"Vectors in collection: {count}")
