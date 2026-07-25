# Dot Desafio Técnico — Backend & IA

API Django REST Framework com LangChain e FAISS para gestão de livros, chatbot com IA generativa e busca semântica com embeddings.

## Stack

| Componente | Tecnologia |
|------------|------------|
| Framework Web | Django 5 + Django REST Framework |
| Banco de Dados | SQLite |
| Chatbot & IA | LangChain + OpenAI (GPT-4o) |
| Observabilidade | LangSmith |
| Vector Store | FAISS (CPU) + sentence-transformers |
| Testes | pytest + pytest-django + APIClient |

## Funcionalidades

### Q1 — API de Livros (CRUD + busca)
- `POST /api/books/` — Cadastrar livro
- `GET /api/books/` — Listar livros (filtro por `title__icontains` e `author__icontains`)
- `GET /api/books/{id}` — Obter livro por ID
- `PUT /api/books/{id}` — Atualizar livro
- `DELETE /api/books/{id}` — Remover livro

### Q2 — Chatbot com IA Generativa
- `POST /api/chat` — Enviar pergunta e obter resposta do GPT-4o como especialista Python
- Integrado com LangSmith para rastreabilidade (opcional)

### Q3 — Busca Semântica com Embeddings
- `POST /api/search` — Enviar texto e obter os 2 documentos mais relevantes com score de similaridade
- Embeddings gerados com `all-MiniLM-L6-v2` e índice FAISS armazenado localmente

## Como executar

```bash
# 1. Ambiente virtual
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate   # Unix

# 2. Dependências
pip install -r requirements.txt

# 3. Variáveis de ambiente
cp .env.example .env
# Edite .env com sua OPENAI_API_KEY e DJANGO_SECRET_KEY

# 4. Migrações
python manage.py migrate

# 5. Servidor de desenvolvimento
python manage.py runserver
```

Acesse a API em `http://localhost:8000/api/`.

## Exemplos de Uso

### Q1 — Criar livro

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Fluente","author":"Luciano Ramalho","publication_date":"2015-08-20","summary":"Python além do básico"}'
```

Response (201):
```json
{
  "id": 1,
  "title": "Python Fluente",
  "author": "Luciano Ramalho",
  "publication_date": "2015-08-20",
  "summary": "Python além do básico"
}
```

### Q1 — Listar livros com filtro

```bash
curl "http://localhost:8000/api/books/?author__icontains=ramalho"
```

### Q2 — Chatbot com IA

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question":"O que são decoradores em Python?"}'
```

Response (200):
```json
{
  "answer": "Decoradores em Python são uma funcionalidade poderosa que permite modificar o comportamento de funções..."
}
```

### Q3 — Busca semântica

```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query":"web framework Python"}'
```

Response (200):
```json
{
  "results": [
    {"document": "FastAPI is a modern web framework...", "score": 0.49},
    {"document": "Python is a high-level...", "score": 0.49}
  ]
}
```

## Testes

```bash
pytest -v
```

Os testes da Q1 usam SQLite em memória e não requerem API keys ou serviços externos.

## Estrutura do projeto

```
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── library/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── ai_chatbot/
│   ├── chatbot_agent.py
│   ├── views.py
│   └── urls.py
├── semantic_search/
│   ├── embeddings_store.py
│   ├── views.py
│   └── urls.py
├── tests/
│   ├── conftest.py
│   └── test_books.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## IA & Inovação

Este projeto utiliza abordagens modernas de IA:

- **RAG (Retrieval-Augmented Generation):** A busca semântica (Q3) permite conectar documentos relevantes ao chatbot (Q2) para respostas contextuais baseadas em conteúdo curado.
- **LangChain:** Framework de orquestração de LLMs utilizado para construir o pipeline de prompt + modelo, com suporte a LangSmith para tracing e observabilidade.
- **Arquitetura MCP (Model Context Protocol):** A estrutura modular da API (apps independentes para cada funcionalidade) permite que cada componente seja exposto como um servidor MCP, seguindo o padrão valorizado pelo DOT Digital Group para integração com assistentes de IA.