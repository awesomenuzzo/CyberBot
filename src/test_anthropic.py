import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables
load_dotenv()

def test_anthropic():
    # Initialize the ChatAnthropic model
    llm = ChatAnthropic(
        model="claude-3-opus-20240229",
        temperature=0,
        max_tokens=1024
    )
    
    # Create a simple message
    response = llm.invoke("Hello! Can you tell me a short joke?")
    
    # Print the response
    print("Response from Claude:")
    print(response.content)

if __name__ == "__main__":
    test_anthropic() 