import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carrega .env da raiz do projeto e da pasta config/
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(BASE_DIR, "config", ".env"))

raw_key = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_KEY = raw_key.strip('"').strip("'").strip()
