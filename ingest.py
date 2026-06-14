import os

# Path to your documents folder
DOCS_PATH = "documents"

# Get list of all .txt files in the documents folder
doc_files = [f for f in os.listdir(DOCS_PATH) if f.endswith(".txt")]

print(f"Found {len(doc_files)} documents:")
for filename in sorted(doc_files):
    print(f"  - {filename}")

def load_document(filepath):
    """Load a document and extract professor metadata from the header."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split header from reviews at the --- REVIEWS --- separator
    parts = content.split("--- REVIEWS ---")
    header = parts[0].strip()
    reviews_text = parts[1].strip() if len(parts) > 1 else ""
    
    # Extract professor name and school from header
    professor = ""
    school = ""
    for line in header.split("\n"):
        if line.startswith("Professor:"):
            professor = line.replace("Professor:", "").strip()
        if line.startswith("School:"):
            school = line.replace("School:", "").strip()
    
    return professor, school, reviews_text

# Test on one file
professor, school, reviews_text = load_document("documents/barker_nathan_suu.txt")
print(f"\nProfessor: {professor}")
print(f"School: {school}")
print(f"Reviews text length: {len(reviews_text)} characters")
print(f"\nFirst 200 characters of reviews:\n{reviews_text[:200]}")

def chunk_reviews(professor, school, reviews_text):
    """Split reviews text into individual chunks."""
    chunks = []
    
    # Split by double newline which separates individual reviews
    raw_reviews = reviews_text.split("\n\n")
    
    for review in raw_reviews:
        review = review.strip()
        
        # Skip empty chunks
        if not review:
            continue
            
        # Skip very short chunks (less than 20 characters)
        if len(review) < 20:
            continue
        
        # Build the full chunk with metadata header
        chunk = f"Professor: {professor} | School: {school}\n{review}"
        chunks.append(chunk)
    
    return chunks

# Test chunking on Nathan Barker
chunks = chunk_reviews(professor, school, reviews_text)
print(f"\nTotal chunks for {professor}: {len(chunks)}")
print(f"\n--- SAMPLE CHUNK 1 ---")
print(chunks[0])
print(f"\n--- SAMPLE CHUNK 2 ---")
print(chunks[1])

# Process all 16 documents
all_chunks = []

for filename in sorted(doc_files):
    filepath = os.path.join(DOCS_PATH, filename)
    professor, school, reviews_text = load_document(filepath)
    chunks = chunk_reviews(professor, school, reviews_text)
    all_chunks.extend(chunks)
    print(f"{professor} ({school}): {len(chunks)} chunks")

print(f"\nTotal chunks across all documents: {len(all_chunks)}")