
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import instruction

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def ask_bot(query):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    message = [{'role': 'system', 'content': instruction},
               {'role': 'user', 'content': query}]
    
    respone=llm.invoke(message)
    
    return respone.content

if __name__ == "__main__":
    print("Welcome to the chat bot!")
    message=ask_bot("can you tell me about the menu?")
    print(message)
