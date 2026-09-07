import logging
import uuid
from fastapi import APIRouter, HTTPException
from core.agent import agent # 🟢 Mudamos para o agente Tutor (mais leve)
from api.chat import ChatRequest

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate")
async def generate_question(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    # Instrução específica para o Tutor apenas BUSCAR uma questão
    prompt_busca = f"Por favor, procure no banco de exercícios uma questão sobre: {request.message}. Apresente o enunciado e as alternativas exatamente como estão no banco."

    try:
        # Usamos o agente tutor que já está configurado para não inventar questões
        result = agent.invoke(
            {"messages": [("user", prompt_busca)]},
            config={"configurable": {"thread_id": session_id}}
        )

        return {
            "session_id": session_id,
            "response": result["messages"][-1].content
        }

    except Exception as exc:
        logger.exception("Erro no processo de busca de questão")
        error_msg = str(exc)
        if "402" in error_msg:
            raise HTTPException(status_code=402, detail="Saldo insuficiente no OpenRouter.")

        raise HTTPException(
            status_code=502,
            detail="O servidor demorou a responder. Tente novamente em instantes."
        )
