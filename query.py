import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# ── Configuration ──────────────────────────────────────────
COLLECTION_NAME = "professor_reviews"

# ── Load embedding model and ChromaDB ──────────────────────
print("Loading model and database...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(COLLECTION_NAME)

# ── Load Groq LLM ───────────────────────────────────────────
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Ready!")

# ── Retrieval function ──────────────────────────────────────
def retrieve(query, k=5):
    """Find the k most relevant chunks for a query."""
    query_embedding = model.encode([query])[0].tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    
    return chunks, metadatas, distances

# ── Generation function ─────────────────────────────────────
def generate(query, chunks, metadatas):
    """Generate a grounded answer using retrieved chunks."""
    
    # Build context from retrieved chunks
    context = ""
    for i, (chunk, metadata) in enumerate(zip(chunks, metadatas)):
        context += f"\n--- Document {i+1} ---\n"
        context += f"Professor: {metadata['professor']} | School: {metadata['school']}\n"
        context += f"{chunk}\n"
    
    # Build the grounded prompt
    system_prompt = """You are a helpful assistant for students researching CS professors at Utah universities.
    
Answer the user's question using ONLY the information provided in the documents below.
Do NOT use any outside knowledge or make assumptions beyond what the documents say.
If the documents don't contain enough information to answer the question, say exactly:
'I don't have enough information in my documents to answer that question.'

Always cite which professor and school your answer draws from."""

    user_prompt = f"""Documents:
{context}

Question: {query}

Answer based only on the documents above:"""

    # Call Groq LLM
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# ── Main ask function ───────────────────────────────────────
def ask(query):
    """Full RAG pipeline: retrieve then generate."""
    chunks, metadatas, distances = retrieve(query)
    answer = generate(query, chunks, metadatas)
    
    sources = list(set([
        f"{m['professor']} ({m['school']})" 
        for m in metadatas
    ]))
    
    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
        "distances": distances
    }

# ── Test the full pipeline ──────────────────────────────────
if __name__ == "__main__":
    print("\n--- TESTING FULL RAG PIPELINE ---\n")
    
    # Test 1 — specific professor question
    result = ask("Is Erin Parker a tough grader?")
    print("Question: Is Erin Parker a tough grader?")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources: {result['sources']}")
    print(f"\nDistances: {[round(d, 3) for d in result['distances']]}")
    
    print("\n" + "="*60 + "\n")
    
    # Test 2 — out of scope question
    result2 = ask("What is the best restaurant near SUU campus?")
    print("Question: What is the best restaurant near SUU campus?")
    print(f"\nAnswer:\n{result2['answer']}")
    print(f"\nSources: {result2['sources']}")