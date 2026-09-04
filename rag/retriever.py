import numpy as np
from google import genai
import os

from rag.vector_store import load_vector_store


# Gemini client
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def retrieve(query, top_k=3):
    """
    Retrieve the most relevant policy chunks for a query.

    Args:
        query (str): User's question.
        top_k (int): Number of chunks to retrieve.

    Returns:
        list: List of dictionaries containing:
            - text: Retrieved policy text
            - source: Source PDF name
            - page: Page number
            - score: Similarity score
    """
    # Create embedding for the user query
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    query_embedding = np.array(
        [response.embeddings[0].values],
        dtype="float32"
    )

    # Load FAISS index and chunks
    index, chunks = load_vector_store()

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_id in zip(scores[0], indices[0]):

        if index_id == -1:
            continue

        chunk = chunks[index_id]

        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"],
            "score": float(score)
        })

    return results


if __name__ == "__main__":

    query = "What is the maximum hotel rate for an Associate?"

    results = retrieve(query)

    print("\nQuery:", query)

    print("\nRetrieved Results:")

    for i, result in enumerate(results, start=1):

        print("\n-----------------------------")
        print("Result:", i)
        print("Score:", result["score"])
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("Text:", result["text"])
