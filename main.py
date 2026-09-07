import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from rag.build_rag import build_question_rag, build_theory_rag

# Alterado: Dando um apelido claro para o router do chat
from api.chat import router as chat_router
from api.gerador import router as generate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    build_question_rag()
    build_theory_rag()
    yield

app = FastAPI(lifespan=lifespan)

# 🟢 Habilita CORS para conexão com o app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo os routers com seus respectivos apelidos
app.include_router(chat_router)
app.include_router(generate_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )
