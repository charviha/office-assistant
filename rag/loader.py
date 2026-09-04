from pathlib import Path
from pypdf import PdfReader


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of the 5 RAG PDFs
POLICY_DIR = BASE_DIR / "data" / "rag_policies"


def load_pdfs():
    documents = []

    for pdf_path in POLICY_DIR.glob("*.pdf"):

        reader = PdfReader(str(pdf_path))

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text and text.strip():

                documents.append({
                    "text": text.strip(),
                    "source": pdf_path.name,
                    "page": page_number
                })

    return documents


if __name__ == "__main__":

    documents = load_pdfs()

    print(f"Total pages loaded: {len(documents)}")

    for doc in documents[:3]:

        print("\n-----------------------------")
        print("Source:", doc["source"])
        print("Page:", doc["page"])
        print("Text:", doc["text"][:300])
