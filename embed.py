import os
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_document, chunk_reviews

# ── Configuration ──────────────────────────────────────────
DOCS_PATH = "documents"
COLLECTION_NAME = "professor_reviews"

# ── Load all chunks from all 16 documents ──────────────────
print("Loading and chunking documents...")

doc_files = [f for f in os.listdir(DOCS_PATH) if f.endswith(".txt")]

all_chunks = []
all_metadata = []

for filename in sorted(doc_files):
    filepath = os.path.join(DOCS_PATH, filename)
    professor, school, reviews_text = load_document(filepath)
    chunks = chunk_reviews(professor, school, reviews_text)
    
    for chunk in chunks:
        all_chunks.append(chunk)
        all_metadata.append({
            "professor": professor,
            "school": school,
            "source": filename
        })

print(f"Total chunks loaded: {len(all_chunks)}")

# ── Set up embedding model ──────────────────────────────────
print("\nLoading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!")

# ── Set up ChromaDB ─────────────────────────────────────────
print("\nSetting up ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_db")

# Delete existing collection if it exists (fresh start)
try:
    client.delete_collection(COLLECTION_NAME)
    print("Deleted existing collection")
except:
    pass

# Create fresh collection
collection = client.create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)
print(f"Created collection: {COLLECTION_NAME}")

# ── Embed and store all chunks ──────────────────────────────
print(f"\nEmbedding {len(all_chunks)} chunks...")
print("This may take a minute...")

# Generate embeddings for all chunks at once
embeddings = model.encode(all_chunks, show_progress_bar=True)

# Store in ChromaDB with unique IDs
collection.add(
    ids=[str(i) for i in range(len(all_chunks))],
    documents=all_chunks,
    embeddings=embeddings.tolist(),
    metadatas=all_metadata
)

print(f"\nSuccessfully stored {collection.count()} chunks in ChromaDB!")

# ── Test retrieval ──────────────────────────────────────────
print("\n--- TESTING RETRIEVAL ---")

def retrieve(query, k=5):
    """Search ChromaDB for most relevant chunks."""
    query_embedding = model.encode([query])[0].tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    return results

# Test query 1
print("\nQuery: 'Is Erin Parker a tough grader?'")
results = retrieve("Is Erin Parker a tough grader?")

for i, (doc, metadata, distance) in enumerate(zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
)):
    print(f"\nResult {i+1} (distance: {distance:.3f})")
    print(f"Source: {metadata['professor']} | {metadata['school']}")
    print(f"Text: {doc[:200]}...")

# Test query 2
print("\nQuery: 'Which professor should I avoid at SUU?'")
results = retrieve("Which professor should I avoid at SUU?")

for i, (doc, metadata, distance) in enumerate(zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
)):
    print(f"\nResult {i+1} (distance: {distance:.3f})")
    print(f"Source: {metadata['professor']} | {metadata['school']}")
    print(f"Text: {doc[:200]}...")

# Test query 3
print("\nQuery: 'What is Gordon Bean like as a professor?'")
results = retrieve("What is Gordon Bean like as a professor?")

for i, (doc, metadata, distance) in enumerate(zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
)):
    print(f"\nResult {i+1} (distance: {distance:.3f})")
    print(f"Source: {metadata['professor']} | {metadata['school']}")
    print(f"Text: {doc[:200]}...")