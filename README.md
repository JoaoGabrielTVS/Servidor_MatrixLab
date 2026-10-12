# Matrix Lab API

API FastAPI do tutor de Álgebra Linear, Matrizes, Vetores e Sistemas Lineares.

## Executar localmente

1. Crie e ative um ambiente virtual Python.
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure `OPENROUTER_API_KEY` no `.env` local ou no ambiente do processo.
4. Inicie a API:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

A documentação interativa fica em `/docs`; a verificação de saúde fica em `/health`.

## Publicar no Render

O arquivo `render.yaml` configura um Web Service com o comando de instalação,
o comando de inicialização e a rota de verificação de saúde. Para publicar:

1. Envie ao GitHub a branch que contém este projeto e o `render.yaml`.
2. No Render, crie um Blueprint conectado ao repositório ou um Web Service
   usando este repositório.
3. Configure a variável secreta `OPENROUTER_API_KEY` no ambiente do serviço
   Render. O arquivo `.env` local não deve ser enviado ao GitHub.
4. Aguarde o deploy e teste `/health`, `/docs` e uma chamada ao `/chat`.

O Render define a porta em `PORT`; o comando de inicialização usa essa variável.
O anúncio mDNS é desativado em produção, pois só serve para descoberta na rede
local.

## API de chat

Envie `POST /chat` com JSON:

```json
{
  "message": "Explique o que é uma matriz identidade"
}
```

Para continuar uma conversa, envie também o `session_id` retornado pela
requisição anterior.

> **Atenção:** `/chat` não possui autenticação nem limite de uso. Antes de
> divulgar o serviço publicamente, implemente controles de acesso e uso para
> evitar chamadas não autorizadas e consumo inesperado da chave do OpenRouter.
