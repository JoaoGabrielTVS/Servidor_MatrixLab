from fastapi import APIRouter
from core.agente_gerador import generator_agent
from api.chat import ChatRequest
import uuid

router = APIRouter()

@router.post("/generate")
async def generate_question(request: ChatRequest):
    # Usa o session_id do request ou cria um novo se não existir
    session_id = request.session_id or str(uuid.uuid4())

    # O invoke agora usa o session_id como thread_id, permitindo memória compartilhada
    result = generator_agent.invoke(
        {"messages": [("user", request.message)]},
        config={"configurable": {"thread_id": session_id}}
    )

    return {
        "session_id": session_id,
        "response": result["messages"][-1].content
    }
