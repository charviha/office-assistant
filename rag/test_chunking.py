from loader import load_pdfs
from chunker import chunk_documents


documents = load_pdfs()

chunks = chunk_documents(documents)


print("Documents/pages:", len(documents))
print("Chunks:", len(chunks))


for i, chunk in enumerate(chunks[:5]):

    print("\n-----------------------------")
    print("Chunk:", i)
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"])
