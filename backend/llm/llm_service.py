import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class LLMService:
    """
    Handles communication with the LLM.
    """

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2,
        )

    def get_llm(self):
        return self.llm