import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from rag.build_rag import build_question_rag, build_theory_rag
from api.chat import router as chat_router
from api.gerador import router as generate_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    build_question_rag()
    build_theory_rag()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(generate_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        timeout_keep_alive=60, # 🟢 Aumenta o tempo de vida da conexão
        proxy_headers=True
    )
