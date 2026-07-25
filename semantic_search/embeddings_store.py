from pathlib import Path
from typing import Any

INDEX_DIR = Path("faiss_index")
INDEX_PATH = INDEX_DIR / "index.faiss"
DOCUMENTS_PATH = INDEX_DIR / "documents.npy"

# Sample documents representing blog posts / articles about programming topics
_DOCUMENTS = [
    "Python is a high-level, general-purpose programming language that emphasizes code readability and simplicity. Created by Guido van Rossum in the late 1980s, it supports multiple programming paradigms including object-oriented and functional programming. Python's extensive standard library and dynamic typing make it one of the most popular languages for beginners and experts alike.",
    "A web framework is a software framework designed to support the development of web applications, web services, and web APIs. Frameworks like Django and Flask provide standard building blocks such as database access, templating, and session management, allowing developers to focus on application logic instead of low-level details.",
    "Object-Relational Mapping (ORM) is a programming technique that converts data between relational databases and object-oriented programming languages. ORMs like SQLAlchemy automate the mapping of database tables to Python objects, handling differences in lifecycle management, references, and inheritance between the two paradigms.",
    "Machine learning is a field of artificial intelligence focused on statistical algorithms that can learn from data and generalize to unseen examples. Advances in deep learning have allowed neural networks to surpass many traditional approaches, powering applications from recommendation systems to natural language processing.",
    "A software design pattern describes a reusable solution to a commonly occurring problem in software design. Patterns like Singleton, Observer, and Factory provide formalized best practices that help developers build maintainable and scalable systems without reinventing the wheel.",
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
    # Convert each document into a 384-dimensional vector
    embeddings = model.encode(_DOCUMENTS, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    # IndexFlatL2 performs brute-force L2 distance search
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
        # Convert L2 distance to similarity score (0 to 1)
        results.append({
            "document": documents[idx],
            "score": float(1 / (1 + dist)),
        })
    return results