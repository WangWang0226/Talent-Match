from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from config import PINECONE_API_KEY
from dotenv import load_dotenv
import os
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

class VectorStore:
    def __init__(self):
        pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = "resume-index"

        # Create index if it doesn't exist
        if self.index_name not in pc.list_indexes().names():
            pc.create_index(
                name=self.index_name,
                dimension=1536,  # dimensionality of OpenAI embeddings
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                
            )

        self.index = pc.Index(self.index_name)
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = PineconeVectorStore(
            index=self.index, embedding=self.embeddings, text_key="text"
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def as_retriever(self):
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 30,  # Increase number of returned documents
                "fetch_k": 100,  # Fetch more documents before filtering
                "include_metadata": True,
            },
        )

    def delete_all_documents(self):
        """Delete all documents from the Pinecone index"""
        try:
            # Delete all vectors in the index
            self.index.delete(delete_all=True)
            print(f"Successfully deleted all documents from index: {self.index_name}")
            return True
        except Exception as e:
            print(f"Error deleting documents from index: {str(e)}")
            return False
