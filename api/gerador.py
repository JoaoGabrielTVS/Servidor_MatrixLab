import logging
import uuid
from fastapi import APIRouter, HTTPException
from core.agent import agent
from core.agente_gerador import generator_agent
from api.chat import ChatRequest

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate")
async def generate_question(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    try:
        # 1. O Tutor tenta selecionar uma questão existente
        tutor_resp = agent.invoke(
            {"messages": [("user", f"Me mostre uma questão sobre: {request.message}")]},
            config=config
        )
        final_text = tutor_resp["messages"][-1].content

        # 2. Verifica se houve ordem de geração (proativa ou urgente)
        if "ESTOQUE_BAIXO" in final_text or "GERAR_AGORA" in final_text:
            # Aciona o Gerador em background/sequencial para repor o estoque
            generator_agent.invoke(
                {"messages": [("user", f"Reponha o estoque conforme a ordem: {final_text}")]},
                config=config
            )
            # Remove a ordem interna do texto final para o usuário não ver a "cozinha"
            final_text = final_text.split('<div style="display:none;">')[0]

        return {
            "session_id": session_id,
            "response": final_text
        }

    except Exception as exc:
        logger.exception("Erro na orquestração de agentes")
        raise HTTPException(status_code=502, detail="Erro ao processar sua solicitação.")
