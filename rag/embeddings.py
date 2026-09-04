import os
import numpy as np
from google import genai


# Create Gemini client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def create_embeddings(chunks):
    """
    Create embeddings for a list of document chunks.

    Each chunk is expected to contain:
        {
            "text": "...",
            "source": "...",
            "page": ...
        }
    """

    embeddings = []

    for chunk in chunks:

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk["text"]
        )

        embedding = response.embeddings[0].values

        embeddings.append(embedding)

    return np.array(embeddings, dtype="float32")


if __name__ == "__main__":

    test_chunks = [
        {
            "text": "Employees must obtain manager approval before business travel.",
            "source": "Travel_Policy.pdf",
            "page": 1
        },
        {
            "text": "Domestic air travel should normally be booked in economy class.",
            "source": "Travel_Policy.pdf",
            "page": 1
        }
    ]

    embeddings = create_embeddings(test_chunks)

    print("Number of chunks:", len(test_chunks))
    print("Embedding shape:", embeddings.shape)
    print("Embedding dimension:", embeddings.shape[1])
