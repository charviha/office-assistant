from loader import load_pdfs
from chunker import chunk_documents
from embeddings import create_embeddings
from vector_store import create_vector_store


def ingest_documents():

    print("Loading PDFs...")

    documents = load_pdfs()

    print("Documents/pages loaded:", len(documents))

    print("\nCreating chunks...")

    chunks = chunk_documents(documents)

    print("Chunks created:", len(chunks))

    print("\nCreating Gemini embeddings...")

    embeddings = create_embeddings(chunks)

    print("Embeddings shape:", embeddings.shape)

    print("\nCreating FAISS vector store...")

    create_vector_store(embeddings, chunks)

    print("\nIngestion completed successfully!")


if __name__ == "__main__":
    ingest_documents()
