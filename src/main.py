import os
from typing import List
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from prompts import SYSTEM_PROMPT, QA_PROMPT

# Load environment variables
load_dotenv()

class RAGBot:
    def __init__(self, documents_path: str = None):
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        self.vectorstore = None
        
        if documents_path:
            self.load_documents(documents_path)
    
    def load_documents(self, documents_path: str):
        """Load and process documents from the specified path"""
        # Load documents
        loader = TextLoader(documents_path)
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
    
    def create_qa_chain(self):
        """Create a QA chain with the vector store"""
        if not self.vectorstore:
            raise ValueError("No documents loaded. Please load documents first.")
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": QA_PROMPT}
        )
    
    def query(self, question: str) -> str:
        """Query the RAG system with a question"""
        qa_chain = self.create_qa_chain()
        response = qa_chain.run(question)
        return response

def main():
    # Example usage
    bot = RAGBot("path/to/your/documents.txt")
    question = "What is the main topic of the document?"
    answer = bot.query(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
