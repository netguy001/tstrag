import chromadb
from sentence_transformers import SentenceTransformer
from config import Config


class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.DATABASE_PATH)
        self.collection = self.client.get_or_create_collection(name="documents")
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)

    def add_chunks(self, chunks, filename):
        """Add chunks to vector database with metadata"""
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk_id": i} for i in range(len(chunks))]
        embeddings = self.model.encode(chunks).tolist()

        self.collection.add(
            ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas
        )

    def search(self, query, top_k=Config.TOP_K_RESULTS):
        """Search for similar chunks"""
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding, n_results=top_k
        )
        return results
