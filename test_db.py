import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="db")
collection = client.get_collection("eqvimech")

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

query = "WOC General Catalog"

query_embedding = embed_model.encode(
    query
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print(results["documents"][0])