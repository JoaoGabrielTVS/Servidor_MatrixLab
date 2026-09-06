from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import OPENROUTER_API_KEY

llm = ChatOpenAI(
    model="deepseek/deepseek-chat", # Nome correto no OpenRouter
        temperature=0.0,
        openai_api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
  
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)