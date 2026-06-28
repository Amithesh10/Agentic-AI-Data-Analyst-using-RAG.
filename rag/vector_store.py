import chromadb
from sentence_transformers import SentenceTransformer
from rag.document_loader import load_document

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()


def chunk_text(text, chunk_size=700, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def build_vector_db(uploaded_files):
    try:
        chroma_client.delete_collection("user_collection")
    except Exception:
        pass

    collection = chroma_client.create_collection("user_collection")

    documents = []
    ids = []

    for file in uploaded_files:
        text = load_document(file)
        chunks = chunk_text(text)

        for chunk in chunks:
            if chunk.strip():
                ids.append(str(len(ids)))
                documents.append(chunk)

    if documents:
        embeddings = embedding_model.encode(documents).tolist()

        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )

    return collection