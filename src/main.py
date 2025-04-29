import os
import time
import warnings
from typing import List, Dict, Optional
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from prompts import SYSTEM_PROMPT, QA_PROMPT, FOLLOW_UP_QUESTIONS_PROMPT, RECOMMENDATION_PROMPT

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set HuggingFace tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()

class CybersecurityRAGBot:
    def __init__(self, documents_path: str = None, model_name: str = "claude-3-opus-20240229"):
        """
        Initialize the Cybersecurity RAG Bot with Claude
        
        Args:
            documents_path: Path to a directory containing cybersecurity knowledge documents
            model_name: Anthropic Claude model to use
        """
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatAnthropic(
            model_name=model_name,
            temperature=0.1,
            max_tokens=4000,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.vectorstore = None
        self.conversation_history = []
        
        if documents_path:
            self.load_documents(documents_path)
    
    def load_documents(self, documents_path: str):
        """
        Load and process documents from the specified path
        
        Args:
            documents_path: Path to a file or directory containing cybersecurity knowledge
        """
        # Check if path is a directory or a file
        if os.path.isdir(documents_path):
            loader = DirectoryLoader(documents_path, glob="**/*.txt")
        else:
            loader = TextLoader(documents_path)
            
        documents = loader.load()
        
        if not documents:
            return
            
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        if not texts:
            return
            
        # Create vector store
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
    
    def retrieve_relevant_context(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve relevant documents from the vector store
        
        Args:
            query: The user query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            return []
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def generate_follow_up_questions(self, query: str, context: List[Document]) -> List[str]:
        """
        Generate follow-up questions based on the user's query and retrieved context
        
        Args:
            query: The user's initial query
            context: Retrieved relevant documents
            
        Returns:
            List of follow-up questions
        """
        try:
            context_text = "\n\n".join([doc.page_content for doc in context])
            
            prompt = PromptTemplate(
                template=FOLLOW_UP_QUESTIONS_PROMPT,
                input_variables=["query", "context"]
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.invoke({"query": query, "context": context_text})
            
            # Handle both dict and string responses
            response_text = response.get('text', '') if isinstance(response, dict) else str(response)
            
            # Parse the response to extract questions
            questions = [q.strip() for q in response_text.split("\n") if q.strip() and "?" in q]
            return questions
        except Exception:
            raise
    
    def generate_recommendation(self, initial_query: str, follow_up_responses: Dict[str, str], context: List[Document]) -> str:
        """
        Generate a comprehensive recommendation based on all gathered information
        
        Args:
            initial_query: The user's initial query
            follow_up_responses: Dictionary of follow-up questions and user responses
            context: Retrieved relevant documents
            
        Returns:
            Detailed recommendation with citations
        """
        context_text = "\n\n".join([doc.page_content for doc in context])
        
        # Format follow-up responses
        follow_up_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in follow_up_responses.items()])
        
        prompt = PromptTemplate(
            template=RECOMMENDATION_PROMPT,
            input_variables=["initial_query", "follow_up_responses", "context"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        recommendation = chain.invoke({
            "initial_query": initial_query,
            "follow_up_responses": follow_up_text,
            "context": context_text
        })
        return recommendation.get('text', '') if isinstance(recommendation, dict) else str(recommendation)
    
    def interactive_session(self):
        """Run an interactive session with the user"""
        print("Welcome to the Cybersecurity RAG Bot!")
        print("Ask a cybersecurity question, and I'll help you find a solution.")
        print("Type 'exit' to quit.\n")
        
        while True:
            # Get initial query
            initial_query = input("\nWhat cybersecurity issue can I help you with today? ")
            if initial_query.lower() == 'exit':
                print("Thank you for using Sentinel. Goodbye!")
                break
            
            # Retrieve relevant context
            print("\nSearching knowledge base...")
            try:
                context = self.retrieve_relevant_context(initial_query)
                
                # Generate follow-up questions
                try:
                    follow_up_questions = self.generate_follow_up_questions(initial_query, context)
                except Exception:
                    print("\nI encountered an error while trying to generate follow-up questions.")
                    print("I'll proceed with generating a recommendation based on your initial query.")
                    follow_up_questions = []
                
                # Ask follow-up questions and collect responses
                follow_up_responses = {}
                for question in follow_up_questions:
                    response = input(f"\n{question} ")
                    follow_up_responses[question] = response
                
                # Generate recommendation
                print("\nGenerating recommendation based on your information...")
                try:
                    recommendation = self.generate_recommendation(initial_query, follow_up_responses, context)
                    
                    # Display recommendation
                    print("\n" + "="*80)
                    print("CYBERSECURITY RECOMMENDATION")
                    print("="*80)
                    print(recommendation)
                    print("="*80)
                except Exception:
                    print("\nI encountered an error while generating the recommendation.")
                
            except Exception:
                print("\nI encountered an unexpected error. Please try again.")

def main():
    """Main function to run the Cybersecurity RAG Bot"""
    # Check for required environment variables
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it in your .env file or environment variables.")
        return
    
    # Use fixed documents path relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    documents_path = os.path.join(os.path.dirname(script_dir), "documents")
    
    if not os.path.exists(documents_path):
        print("Error: Documents directory does not exist.")
        return
    
    # Initialize and run the bot
    bot = CybersecurityRAGBot(documents_path)
    bot.interactive_session()

if __name__ == "__main__":
    main()