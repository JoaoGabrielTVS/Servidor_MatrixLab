import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from network.mdns import start_mdns
from api.chat import router as chat_router

zeroconf_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global zeroconf_instance
    if os.getenv("APP_ENV") == "production" or os.getenv("RENDER_SERVICE_ID"):
        print("mDNS desativado: serviço executando no Render.")
    else:
        zeroconf_instance = await asyncio.to_thread(start_mdns)
    yield
    if zeroconf_instance:
        print("Encerrando anúncio mDNS zeroconf...")
        try:
            await asyncio.to_thread(zeroconf_instance.close)
        except Exception as e:
            print(f"Erro ao fechar zeroconf: {e}")

app = FastAPI(title="Agente Tutor - Matrix Lab", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Agente Tutor Matrix Lab"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        timeout_keep_alive=60,
        proxy_headers=True
    )
