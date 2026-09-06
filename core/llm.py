from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_API_KEY
from core.embeddings import LightweightEmbeddings

llm = ChatOpenAI(
    model="deepseek/deepseek-chat", # Nome correto no OpenRouter
        temperature=0.0,
        openai_api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
  
)

embeddings = LightweightEmbeddings()


def get_embeddings():
    return embeddings