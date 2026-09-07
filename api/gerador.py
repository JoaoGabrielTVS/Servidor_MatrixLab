import logging
import uuid

from fastapi import APIRouter, HTTPException
from core.agente_gerador import generator_agent
from api.chat import ChatRequest

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate")
async def generate_question(request: ChatRequest):
    # Usa o session_id do request ou cria um novo se não existir
    session_id = request.session_id or str(uuid.uuid4())

    # O invoke agora usa o session_id como thread_id, permitindo memória compartilhada
    try:
        result = generator_agent.invoke(
            {"messages": [("user", request.message)]},
            config={"configurable": {"thread_id": session_id}}
        )
    except Exception as exc:
        logger.exception("Falha ao gerar questão para a sessão %s", session_id)
        raise HTTPException(
            status_code=502,
            detail=f"Falha ao gerar questão: {type(exc).__name__}: {exc}"
        ) from exc

    return {
        "session_id": session_id,
        "response": result["messages"][-1].content
    }
