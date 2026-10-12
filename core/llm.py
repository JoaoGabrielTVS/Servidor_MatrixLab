import os
from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_API_KEY

api_key = OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "").strip('"').strip("'")

MODEL_NAME = os.getenv("MODEL_NAME", "deepseek/deepseek-chat")

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0.2,
    api_key=api_key if api_key else "missing_key",
    openai_api_key=api_key if api_key else "missing_key",
    base_url="https://openrouter.ai/api/v1",
    max_tokens=2048
)
