import faiss
import numpy as np
import json
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Where FAISS files will be stored
VECTOR_DIR = BASE_DIR / "data" / "vector_store"

VECTOR_DIR.mkdir(parents=True, exist_ok=True)


def create_vector_store(embeddings, chunks):
    """
    Create a FAISS vector index and save it along with
    the corresponding chunk metadata.
    """

    # Make sure embeddings are float32
    embeddings = np.asarray(embeddings, dtype="float32")

    # Embedding dimension
    dimension = embeddings.shape[1]

    # FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Add vectors
    index.add(embeddings)

    # Save FAISS index
    index_path = VECTOR_DIR / "office_assistant.index"
    faiss.write_index(index, str(index_path))

    # Save chunks/metadata
    metadata_path = VECTOR_DIR / "chunks.json"

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print("FAISS index created successfully")
    print("Number of vectors:", index.ntotal)
    print("Embedding dimension:", dimension)
    print("Index saved to:", index_path)
    print("Metadata saved to:", metadata_path)


def load_vector_store():
    """
    Load the FAISS index and chunk metadata.
    """

    index_path = VECTOR_DIR / "office_assistant.index"
    metadata_path = VECTOR_DIR / "chunks.json"

    index = faiss.read_index(str(index_path))

    with open(metadata_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return index, chunks
