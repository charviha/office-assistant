import os
from google import genai

from retriever import retrieve


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def answer_question(question, top_k=3):

    # Retrieve relevant chunks
    results = retrieve(question, top_k=top_k)

    # Build context
    context = ""

    for result in results:
        context += f"""
Source: {result['source']}
Page: {result['page']}

{result['text']}

-----------------------------
"""

    # Prompt Gemini
    prompt = f"""
You are an Office Assistant for Novatrix Technologies.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I could not find this information in the company documents."

Do not make up information.

Context:
{context}

User Question:
{question}

Provide a concise and clear answer.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    question = "What is the maximum hotel rate for an Associate?"

    answer = answer_question(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)
