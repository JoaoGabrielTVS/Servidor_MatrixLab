import re
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.agent import agent
from config.settings import OPENROUTER_API_KEY

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

def converter_latex_para_texto(texto: str) -> str:
    texto = texto.replace("```html", "").replace("```", "").strip()
    texto = re.sub(r'<[^>]+>', '', texto)

    # Converte matrizes LaTeX \begin{pmatrix} a & b \\ c & d \end{pmatrix} -> [ a  b / c  d ]
    texto = re.sub(
        r'\\begin\{(?:pmatrix|matrix|bmatrix)\}(.*?)\\end\{(?:pmatrix|matrix|bmatrix)\}',
        lambda m: "[ " + m.group(1).replace(r'\\', ' / ').replace('&', '  ').strip() + " ]",
        texto, flags=re.DOTALL
    )

    texto = texto.replace(r'\[', '').replace(r'\]', '').replace(r'\(', '').replace(r'\)', '')
    texto = texto.replace(r'\text{det}', 'det').replace(r'\text', '')

    while r'\sqrt{' in texto:
        texto = re.sub(r'\\sqrt\{([^}]+)\}', r'√(\1)', texto)
    texto = texto.replace(r'\sqrt', '√')

    while r'\frac{' in texto:
        texto = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1 / \2)', texto)

    substituicoes = {
        r'\cdot': '·',
        r'\times': '×',
        r'\theta': 'θ',
        r'\cos': 'cos',
        r'\sin': 'sin',
        r'\tan': 'tan',
        r'\lambda': 'λ',
        r'\det': 'det',
        r'\neq': '≠',
        r'\approx': '≈',
        r'\le': '≤',
        r'\ge': '≥',
        r'\pm': '±',
        '$$': '',
        '$': ''
    }

    for latex, simbolo in substituicoes.items():
        texto = texto.replace(latex, simbolo)

    return texto.strip()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "missing_key":
        raise HTTPException(
            status_code=402,
            detail="OPENROUTER_API_KEY não encontrada! Crie o arquivo .env com OPENROUTER_API_KEY."
        )

    session_id = request.session_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    try:
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config=config,
            timeout=120
        )
        conteudo = str(response["messages"][-1].content)
        conteudo_formatado = converter_latex_para_texto(conteudo)
    except Exception as exc:
        error_msg = str(exc)
        if "401" in error_msg or "402" in error_msg or "credits" in error_msg.lower() or "User not found" in error_msg:
            raise HTTPException(
                status_code=402,
                detail="Chave do OpenRouter inválida ou sem saldo. Verifique sua chave no arquivo .env."
            )
        raise HTTPException(
            status_code=502,
            detail=f"Erro de conexão com o modelo de IA: {error_msg}"
        )

    resultado = {
        "session_id": session_id,
        "response": conteudo_formatado
    }
    return resultado
