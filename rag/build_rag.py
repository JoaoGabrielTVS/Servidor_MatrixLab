from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

import os

from core.llm import get_embeddings
from config.settings import QUESTION_BANK_PATH, THEORY_BANK_PATH

# Adicionamos o vectorstore globalmente aqui para podermos manipular depois
question_vectorstore = None
question_retriever = None
theory_retriever = None

def build_question_rag():
    global question_retriever, question_vectorstore
    embeddings = get_embeddings()

    print("Construindo RAG de questões...")
    docs = []

    if not os.path.exists(QUESTION_BANK_PATH):
        os.makedirs(QUESTION_BANK_PATH, exist_ok=True)

    for file_name in os.listdir(QUESTION_BANK_PATH):
        if file_name.endswith(".txt"):
            file_path = os.path.join(QUESTION_BANK_PATH, file_name)
            loader = TextLoader(file_path, encoding="utf-8")
            loaded_docs = loader.load()

            for doc in loaded_docs:
                doc.metadata["source"] = file_name
            docs.extend(loaded_docs)

    # Se a pasta estiver vazia no primeiro início, cria um RAG vazio ou com aviso
    if not docs:
        print("Aviso: Banco de questões vazio. Inicializando RAG limpo.")
        question_vectorstore = Chroma(
            collection_name="question_rag",
            embedding_function=embeddings,
            persist_directory="./chroma/chroma_questions"
        )
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        chunks = splitter.split_documents(docs)

        question_vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="question_rag",
            persist_directory="./chroma/chroma_questions"
        )

    question_retriever = question_vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4}
    )
    print("RAG de questões construído com sucesso!")


def add_new_question_to_rag(file_name: str, content: str):
    """
    Função para adicionar dinamicamente uma nova questão ao banco vetorial 
    sem reiniciar a aplicação.
    """
    global question_vectorstore, question_retriever
    
    if question_vectorstore is None:
        print("Erro: RAG de questões não foi inicializado ainda.")
        return

    print(f"Adicionando nova questão '{file_name}' ao RAG dinamicamente...")

    # 1. Cria o documento LangChain com os metadados corretos
    new_doc = Document(
        page_content=content,
        metadata={"source": file_name}
    )

    # 2. Divide em chunks igualzinho ao build inicial
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    chunks = splitter.split_documents([new_doc])

    # 3. Adiciona diretamente ao Chroma existente
    question_vectorstore.add_documents(chunks)
    print("Nova questão indexada com sucesso no RAG!")


def build_theory_rag():
    global theory_retriever
    embeddings = get_embeddings()

    print("Construindo RAG de teoria...")
    docs = []

    if not os.path.exists(THEORY_BANK_PATH):
        os.makedirs(THEORY_BANK_PATH, exist_ok=True)

    for file_name in os.listdir(THEORY_BANK_PATH):
        if file_name.endswith(".txt"):
            file_path = os.path.join(THEORY_BANK_PATH, file_name)
            loader = TextLoader(file_path, encoding="utf-8")
            loaded_docs = loader.load()

            for doc in loaded_docs:
                doc.metadata["source"] = file_name
            docs.extend(loaded_docs)

    if not docs:
        print("Aviso: Banco de teoria vazio.")
        vectorstore = Chroma(
            collection_name="theory_rag",
            embedding_function=embeddings,
            persist_directory="./chroma/chroma_theory"
        )
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="theory_rag",
            persist_directory="./chroma/chroma_theory"
        )

    theory_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4}
    )
    print("RAG de teoria construído com sucesso!")