from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from core.agent import agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):

    session_id = request.session_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.message
                    }
                ]
            },
            config=config,
            timeout=120
        )
    except Exception as exc:
        error_msg = str(exc)
        if "402" in error_msg or "credits" in error_msg.lower():
            raise HTTPException(
                status_code=402,
                detail="Saldo insuficiente no OpenRouter. Por favor, verifique seus créditos."
            )
        raise HTTPException(
            status_code=502,
            detail="O servidor demorou muito para responder ou encontrou um erro interno. Tente novamente em instantes."
        )

    return {
        "session_id": session_id,
        "response": response["messages"][-1].content
    }
