# Project Planning: The Unofficial Guide — Utah CS Professor Reviews

## Domain

The domain for this project is student reviews of CS professors at Southern Utah University (SUU), University of Utah, Brigham Young University (BYU), and Utah State University — covering teaching quality, exam difficulty, grading, and workload.

This kind of student knowledge is difficult to find through official channels because universities have an interest in protecting both their institution and their faculty. Official sources like course catalogs and faculty pages present professors in the best possible light — they won't tell you that a professor's exam averages are consistently below 50%, or that students feel talked down to in class. Sharing that kind of information publicly could discourage enrollment, create bias against faculty, or expose the university to complaints. The real student experience lives in informal spaces like Rate My Professors — places students share with each other, not with administrators.

---

## Documents

16 source documents collected from Rate My Professors, covering CS professors across 4 Utah universities. All documents are stored as cleaned .txt files with one review per entry.

| # | Professor | School | URL | Reviews |
|---|-----------|--------|-----|---------|
| 1 | Nathan Barker | Southern Utah University | https://www.ratemyprofessors.com/professor/1034793 | 23 |
| 2 | Cecily Heiner | Southern Utah University | https://www.ratemyprofessors.com/professor/1719474 | 25 |
| 3 | Hussain Aljafer | Southern Utah University | https://www.ratemyprofessors.com/professor/2574740 | 13 |
| 4 | Prosenjit Chatterjee | Southern Utah University | https://www.ratemyprofessors.com/professor/2997290 | 19 |
| 5 | John Regehr | University of Utah | https://www.ratemyprofessors.com/professor/762698 | 17 |
| 6 | Erin Parker | University of Utah | https://www.ratemyprofessors.com/professor/710755 | 181 |
| 7 | Daniel Kopta | University of Utah | https://www.ratemyprofessors.com/professor/1799826 | 122 |
| 8 | Aditya Bhaskara | University of Utah | https://www.ratemyprofessors.com/professor/2252159 | 28 |
| 9 | Gordon Bean | Brigham Young University | https://www.ratemyprofessors.com/professor/2781547 | 52 |
| 10 | Cory Barker | Brigham Young University | https://www.ratemyprofessors.com/professor/50662 | 142 |
| 11 | Duane Dougal | Brigham Young University | https://www.ratemyprofessors.com/professor/2114854 | 20 |
| 12 | Tom Stephens | Brigham Young University | https://www.ratemyprofessors.com/professor/3064932 | 17 |
| 13 | Erik Falor | Utah State University | https://www.ratemyprofessors.com/professor/2276652 | 74 |
| 14 | Vicki Allan | Utah State University | https://www.ratemyprofessors.com/professor/795934 | 51 |
| 15 | Joseph Ditton | Utah State University | https://www.ratemyprofessors.com/professor/2590785 | 37 |
| 16 | Seth Bassetti | Utah State University | https://www.ratemyprofessors.com/professor/2930654 | 18 |

**Total: ~840 reviews across 4 schools**

---

## Chunking Strategy

**Strategy:** One review per chunk.

**Chunk size:** One individual student review (typically 2-5 sentences, roughly 50-150 words).

**Overlap:** None. Reviews are already independent units — there is no context that bleeds between one review and the next, so overlap adds no value here.

**Metadata header on every chunk:**
Each chunk includes a metadata header with professor name, school, course, quality rating, and difficulty rating so that every chunk is fully self-contained and retrievable without needing surrounding context.

Example chunk:
```
Professor: Erin Parker | School: University of Utah | Course: CS2420 | Date: May 2026 | Quality: 3.0 | Difficulty: 4.0

Overall she is a good teacher and probably the best one to teach CS2420. However she is a very tough grader and nitpicky. Apply yourself from the beginning of the semester and you should pass. Don't be afraid to ask questions. She knows the material very well.
```

**Why this fits the documents:**
Reviews are short, opinion-based, and self-contained. Each review represents one student's complete experience — splitting them further would destroy meaning, and grouping them together would dilute specificity. A query like "Is Parker a tough grader?" needs to match a review specifically about grading, not a chunk that mixes grading with office hours and exam format. One review per chunk gives the embedding model the most focused, specific semantic signal possible.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via sentence-transformers. Runs locally with no API key or rate limits. Produces 384-dimensional vectors. Uses cosine similarity to find semantically similar chunks — measuring the angle between vectors rather than raw distance, which means meaning is preserved regardless of review length.

**Vector store:** ChromaDB, running locally with no account needed.

**Top-k:** k=5. Retrieving 5 chunks gives the LLM enough context from multiple student perspectives without diluting the response with loosely related material.

**Production tradeoffs:** If deploying this system for real users, the following tradeoffs would be worth considering:
- **Context length:** all-MiniLM-L6-v2 handles up to 256 tokens — sufficient for individual reviews but may truncate very long ones. OpenAI's text-embedding-3-large supports up to 8191 tokens.
- **Multilingual support:** all-MiniLM-L6-v2 is English-only. A multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be needed for non-English reviews.
- **Accuracy:** Larger models like text-embedding-3-large produce higher quality embeddings but cost money and require API calls.
- **Latency:** Local models like all-MiniLM-L6-v2 are faster since there is no network call.

---

## Evaluation Plan

| # | Question | Expected Answer |
|---|----------|----------------|
| Q1 | Which CS professor should I avoid at SUU and why? | Hussain Aljafer — tests consistently cover material never taught in lectures, exam averages around 50%, refuses to help students claiming it would give away answers, not recommended for beginners. |
| Q2 | Who is the best CS professor at BYU if you care about learning the material and why? | Gordon Bean — explains difficult concepts clearly, re-explains from different angles until everyone understands, genuinely cares about student success, 93% would take again. |
| Q3 | Which CS professors should I take at University of Utah for an easy A? | None — all four U of U professors in the dataset are known for heavy workloads and tough grading. Parker is a notoriously harsh grader, Kopta has heavy assignments and difficult exams, Regehr assigns dense reading, and Bhaskara has disorganized lectures that make it hard to prepare for tests. |
| Q4 | What should I know before taking Professor Seth Bassetti and what study strategies should I use? | Lectures are fast-paced so keep up and don't fall behind. Exams are open note so take detailed notes in class. Projects range from easy to surprisingly difficult so always start early. He is very accessible during office hours. Asking questions in class is key to success. |
| Q5 | Based on student reviews, which CS department has the most consistently positive reviews — BYU or Utah State? | Expected partial failure — system may struggle to synthesize and compare reviews across multiple professors and schools simultaneously. This serves as the documented failure case. |

---

## Anticipated Challenges

**Challenge 1 — Same last name professors across schools:**
Two professors in the dataset share the last name Barker — Nathan Barker at SUU and Cory Barker at BYU. A query like "Is Professor Barker a good teacher?" could retrieve chunks from both professors and produce a mixed or inaccurate response that blends reviews from two completely different people at two different schools.

**Challenge 2 — Uneven review counts causing sampling bias:**
Professors in the dataset have vastly different numbers of reviews, ranging from 13 (Hussain Aljafer) to 181 (Erin Parker). The retrieval system always returns k=5 chunks regardless of how many total reviews a professor has. This means for a professor with 13 reviews, 5 chunks represent 38% of their entire review history, while for Parker, 5 chunks represent only 2.7%. The LLM generates answers with equal confidence in both cases, which could be misleading — a small sample of negative reviews about a lesser-known professor could unfairly define the system's answer about them.

---

## AI Tool Plan

**Stage 1 — Document loading and chunking:**
I will prompt Claude with my Documents section, my Chunking Strategy section, and a sample of my .txt file format and ask it to implement a Python script that loads all 16 files and splits them into individual review chunks with metadata headers attached to each chunk.

**Stage 2 — Embedding and ChromaDB storage:**
I will prompt Claude with my Retrieval Approach section and my pipeline architecture diagram and ask it to implement the embedding step using all-MiniLM-L6-v2 via sentence-transformers, storing all chunks in ChromaDB with source metadata (professor name and school) attached to each entry.

**Stage 3 — Retrieval function:**
I will prompt Claude with my Retrieval Approach section and ask it to implement a retrieval function that accepts a query string, converts it to an embedding, performs cosine similarity search in ChromaDB, and returns the top k=5 most relevant chunks along with their source professor name and school.

**Stage 4 — Generation and Gradio interface:**
I will prompt Claude with my grounding requirement (answer from retrieved chunks only, with source attribution) and the Gradio skeleton from the assignment instructions and ask it to wire retrieval and generation together, ensuring the system explicitly declines to answer questions not covered by the documents.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DOCUMENT INGESTION                   │
│        16 .txt files (~840 reviews across 4 schools)    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                      CHUNKING                           │
│         One review = one chunk                          │
│         Metadata header: professor, school,             │
│         course, quality rating, difficulty rating       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              EMBEDDING + VECTOR STORE                   │
│         Model: all-MiniLM-L6-v2                        │
│         Store: ChromaDB (local)                         │
│         ~840 chunks stored as vectors                   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                     RETRIEVAL                           │
│         User query → embedded → cosine similarity       │
│         Top k=5 most relevant chunks returned           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    GENERATION                           │
│         LLM: Groq llama-3.3-70b-versatile              │
│         Grounded prompt: answer from chunks only        │
│         Response includes source attribution            │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
                 USER ANSWER
            (with cited sources)
```
