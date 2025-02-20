import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from datetime import datetime, timedelta

class PDFProcessor:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name="gpt-4")
        self.retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    def process_pdf(self, file_path):
        filename = os.path.basename(file_path)

        loader = PyPDFLoader(file_path=file_path)
        documents = loader.load()

        # Add metadata to each document
        for doc in documents:
            doc.metadata["source"] = filename
            doc.metadata["resume_id"] = filename

        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=30, separator="\n"
        )
        docs = text_splitter.split_documents(documents=documents)

        # Store in Pinecone
        self.vector_store.add_documents(docs)

    def query_documents(self, query):
        custom_prompt = """You have been given multiple resumes, each identified by a unique resume_id. The system has already provided their contents. 
            Here are the details of the job opening: {query}
            Task:
            1. Compare their work experience, skills, education into a table, markdown format.
            2. Determine which resume is the best match for this position. Provide a concise conclusion about your choice.
            3. Offer three clear, specific reasons that justify why this resume is the most suitable, drawing on the details provided in the resumes.
            Make sure your answer is well-structured and references relevant information from the resumes whenever possible.
        """
        combine_docs_chain = create_stuff_documents_chain(
            self.llm, self.retrieval_qa_chat_prompt
        )
        retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(), combine_docs_chain
        )

        response = retrieval_chain.invoke({"input": custom_prompt.format(query=query)})
        return response["answer"]
    
    def ask(self, query):
        combine_docs_chain = create_stuff_documents_chain(
            self.llm, self.retrieval_qa_chat_prompt
        )
        retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(), combine_docs_chain
        )

        response = retrieval_chain.invoke({"input": query})
        return response["answer"]


    def cleanup_old_files(self, hours=24):
        """Clean up files older than specified hours"""
        try:
            current_time = datetime.now()
            for filename in os.listdir(self.upload_folder):
                file_path = os.path.join(self.upload_folder, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                if current_time - file_modified > timedelta(hours=hours):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")