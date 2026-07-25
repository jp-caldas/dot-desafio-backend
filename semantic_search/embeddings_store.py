from pathlib import Path
from typing import Any

INDEX_DIR = Path("faiss_index")
INDEX_PATH = INDEX_DIR / "index.faiss"
DOCUMENTS_PATH = INDEX_DIR / "documents.npy"

_DOCUMENTS = [
    "Python is a high-level, interpreted programming language known for its readability and versatility.",
    "FastAPI is a modern web framework for building APIs with Python, based on Starlette and Pydantic.",
    "SQLAlchemy is an SQL toolkit and Object-Relational Mapping (ORM) library for Python.",
    "LangChain is a framework for developing applications powered by language models, enabling chaining and orchestration.",
    "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.",
]

_model: Any = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def build_index() -> int:
    import faiss
    import numpy as np

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    model = _get_model()
    embeddings = model.encode(_DOCUMENTS, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    faiss.write_index(index, str(INDEX_PATH))
    np.save(str(DOCUMENTS_PATH), np.array(_DOCUMENTS, dtype=object))
    return index.ntotal


def load_index() -> tuple[Any, list[str]]:
    import faiss
    import numpy as np

    if not INDEX_PATH.exists():
        count = build_index()
        if count == 0:
            raise RuntimeError("No documents indexed")
    index = faiss.read_index(str(INDEX_PATH))
    documents = np.load(str(DOCUMENTS_PATH), allow_pickle=True).tolist()
    return index, documents


def search(query: str, k: int = 2) -> list[dict]:
    import numpy as np

    index, documents = load_index()
    model = _get_model()
    query_embedding = model.encode([query], convert_to_numpy=True).astype(np.float32)
    distances, indices = index.search(query_embedding, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append({
            "document": documents[idx],
            "score": float(1 / (1 + dist)),
        })
    return results