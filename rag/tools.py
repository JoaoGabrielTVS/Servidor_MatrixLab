import os
import re
from datetime import datetime
from langchain.tools import tool
import rag.build_rag as build_rag
from config.settings import QUESTION_BANK_PATH # Usando o seu caminho centralizado


# Garante que o caminho use a variável centralizada do sistema
# Mas caso falte, mantém o fallback seguro para a árvore local
QUESTOES_GERADAS_PATH = os.path.join(os.path.dirname(__file__), "questoes_geradas")

@tool
def search_exercises(query: str) -> str:
    """
    Busca exercícios, listas, problemas e questões
    de álgebra linear e vetorial.

    Use esta ferramenta SEMPRE que o usuário:
    - pedir uma questão
    - pedir exercícios
    - pedir listas
    - pedir problemas
    - pedir exemplos práticos
    """

    if build_rag.question_retriever is None:
        return "RAG de questões não inicializado."

    # 🟢 Limitamos a busca para apenas 2 documentos para economizar tokens e ser mais rápido
    docs = build_rag.question_retriever.invoke(query)[:2]

    if not docs:
        return "Nenhuma questão encontrada."

    context = "\n\n".join([
        f"[Fonte: {doc.metadata.get('source', 'desconhecida')}]\n{doc.page_content}"
        for doc in docs
    ])

    return context


@tool
def search_theory(query: str) -> str:
    """
    Busca teoria, definições e explicações
    de álgebra linear e vetorial.

    Use esta ferramenta para:
    - conceitos
    - definições
    - explicações
    """

    if build_rag.theory_retriever is None:
        return "RAG de teoria não inicializado."

    # 🟢 Limitamos a busca para apenas 2 documentos para economizar tokens e ser mais rápido
    docs = build_rag.theory_retriever.invoke(query)[:2]

    if not docs:
        return "Nenhuma teoria encontrada."

    context = "\n\n".join([
        f"[Fonte: {doc.metadata.get('source', 'desconhecida')}]\n{doc.page_content}"
        for doc in docs
    ])

    return context

# tools.py — adicionar
@tool
def save_question(content: str, assunto: str) -> str:
    """
    Salva uma nova questão gerada no banco de questões (.txt) dentro da pasta
    configurada organizando pelo assunto, e a adiciona imediatamente ao RAG.

    Parâmetros:
    - content: O texto completo da questão gerada.
    - assunto: O assunto/tema da questão (ex: 'Matriz Inversa').
    """
    # 1. Garante que a pasta configurada (questoes_geradas) existe fisicamente
    os.makedirs(QUESTION_BANK_PATH, exist_ok=True)
    
    # 2. Limpa o nome do assunto para não quebrar o Linux
    assunto_limpo = assunto.lower().strip()
    assunto_limpo = re.sub(re.compile(r'[^\w\s-]'), '', assunto_limpo)
    assunto_limpo = re.sub(re.compile(r'[-\s]+'), '_', assunto_limpo)
    
    # 3. Cria o nome do arquivo com o assunto e timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{assunto_limpo}_{timestamp}.txt"
    path = os.path.join(QUESTION_BANK_PATH, filename)

    # 4. Salva o arquivo fisicamente na pasta correta
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    # 5. 🔥 Alimenta o RAG em tempo real
    try:
        build_rag.add_new_question_to_rag(file_name=filename, content=content)
        return f"Questão sobre '{assunto}' salva com sucesso em '{filename}' e injetada no RAG!"
    except Exception as e:
        return f"Questão salva em '{filename}', mas houve um erro ao atualizar o RAG: {e}"