import os

from dotenv import load_dotenv

load_dotenv()


# Definicão da chave API (chave real deve ser armazenada em um arquivo .env)
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

# Definição do caminho para banco de questões
QUESTION_BANK_PATH = os.getenv(
    "QUESTION_BANK_PATH",
    "rag/question_bank"
)
# Definição do caminho para banco de teoria
THEORY_BANK_PATH = os.getenv(
    "THEORY_BANK_PATH",
    "rag/theory_bank"
)