# The Unofficial Utah CS Professor Guide

A RAG (Retrieval-Augmented Generation) system that makes student-generated knowledge about CS professors at Utah universities searchable and answerable. Users ask plain-language questions and get grounded, cited answers drawn from real Rate My Professors reviews.

---

## Domain and Document Sources

**Domain:** Student reviews of CS professors at Southern Utah University (SUU), University of Utah, BYU, and Utah State University — covering teaching quality, exam difficulty, grading, and workload.

This kind of student knowledge is difficult to find through official channels because universities have an interest in protecting both their institution and their faculty. Official sources like course catalogs and faculty pages present professors in the best possible light — they won't tell you that a professor's exam averages are consistently below 50%, or that students feel talked down to in class. The real student experience lives in informal spaces like Rate My Professors.

### Source Documents (16 total, ~782 reviews)

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

Documents were collected manually by copying review text from Rate My Professors into cleaned .txt files. This approach was chosen over scraping because RMP uses JavaScript rendering that blocks automated requests.

**Document selection methodology:** A minimum of 12 reviews per professor was required to ensure sufficient data for meaningful retrieval. Diversity of opinions was deliberately prioritized over volume — for example, choosing a professor with 17 mixed reviews over one with 50+ strongly skewed positive reviews. This decision was made because diverse perspectives produce richer and more varied chunks for the embedding model to work with. A professor with 50 uniformly glowing reviews would produce semantically similar chunks that cluster together, reducing retrieval variety. Mixed reviews covering different aspects (grading, teaching style, exam difficulty, workload) give the system more distinct semantic signals to match against different query types.

**Sampling bias note:** Professors in the dataset have vastly different review counts (13 to 181). Since the system always retrieves k=5 chunks regardless, professors with fewer reviews are over-represented per query. For Hussain Aljafer (13 reviews), 5 chunks represent 38% of his entire review history. For Erin Parker (181 reviews), 5 chunks represent only 2.7%. The LLM generates answers with equal confidence in both cases, which can be misleading for lesser-known professors with small sample sizes.

---

## Chunking Strategy and Reasoning

**Strategy:** One review per chunk, with no overlap.

**Chunk size:** One individual student review (typically 50–150 words).

**Overlap:** None. Reviews are already independent units — there is no context that bleeds between one review and the next, so overlap adds no value here.

**Metadata header on every chunk:** Each chunk includes professor name, school, course, quality rating, difficulty rating, and date so that every chunk is fully self-contained and retrievable without needing surrounding context.

**Why this fits the documents:** Reviews are short, opinion-based, and self-contained. Each review represents one student's complete experience. Splitting them further would destroy meaning, and grouping them together would dilute specificity. A query like "Is Parker a tough grader?" needs to match a review specifically about grading, not a chunk that mixes grading with office hours and exam format. One review per chunk gives the embedding model the most focused, specific semantic signal possible.

**Total chunks produced:** 782 (slightly fewer than total ratings because very short reviews under 20 characters were filtered out — these were ratings with no written text).

---

## Sample Chunks

**Chunk 1 — Source: parker_erin_uofu.txt**
```
Professor: Erin Parker | School: University of Utah
Course: CS2420 | Date: Oct 30, 2020 | Quality: 3.0 | Difficulty: 4.0 | Grade: B | Would Take Again: No
She's a nitpicky grader when it comes to exams. You're never 100% confident if your answers satisfies her. Even if your answer is almost correct she may refuse partial credit. She grades written responses open ended. One small mistake and she deducts a lot. Your answer can't just be right, it has to be right specifically to her satisfaction.
```

**Chunk 2 — Source: bean_gordon_byu.txt**
```
Professor: Gordon Bean | School: Brigham Young University
Course: CS235 | Date: Apr 24, 2025 | Quality: 5.0 | Difficulty: 4.0 | Grade: A | Would Take Again: Yes
This is the second class I have taken from Dr. Bean and there is a reason I keep coming back. Not only is he excellent at explaining new topics but he is also very willing to go back and explain things another way until everyone understands. Around 2 hw/week, unit progress checks, 1 midterm, and a final similar to progress checks.
```

**Chunk 3 — Source: aljafer_hussain_suu.txt**
```
Professor: Hussain Aljafer | School: Southern Utah University
Course: CS1400 | Date: Dec 7, 2020 | Quality: 1.0 | Difficulty: 4.0 | Would Take Again: No
DON'T TAKE THIS CLASS WITH THIS PROFESSOR IF IT'S YOUR FIRST CODING CLASS AND YOU KNOW YOU ARE GOING TO NEED HELP. Very vague in his explanations, never touches everything that will be on the test, and if you ask him for help he always says he can't help because he would give away the answer. Made my semester so miserable.
```

**Chunk 4 — Source: bassetti_seth_usu.txt**
```
Professor: Seth Bassetti | School: Utah State University
Course: CS1400 | Date: Apr 8, 2025 | Quality: 5.0 | Difficulty: 2.0 | Grade: A | Would Take Again: Yes
Seth is awesome. Not only does he know his stuff, he explains it very well. He is a great presenter, super fun to listen to, and walks through examples in class. If you don't understand something, he takes time to explain it. If you're stuck on a project you can also visit him during office hours and he is happy to help you find and fix your bugs.
```

**Chunk 5 — Source: kopta_daniel_uofu.txt**
```
Professor: Daniel Kopta | School: University of Utah
Course: CS3810 | Date: Dec 13, 2025 | Quality: 5.0 | Difficulty: 4.0 | Grade: B | Would Take Again: Yes
I would say that Kopta has been the best professor I've had at the U. He's very knowledgeable and I'm happy he's the one teaching 3810. If it would be anyone else the class would be magnitudes more difficult. His lectures go into detail and he makes sure that you are understanding the material.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers. Runs locally with no API key or rate limits. Produces 384-dimensional vectors using cosine similarity.

**Why cosine similarity over euclidean distance:** Cosine similarity measures the angle between vectors rather than raw distance. This means meaning is preserved regardless of review length — a short and a long review about the same topic both point in the same direction semantically.

**Production tradeoffs:**
- **Context length:** all-MiniLM-L6-v2 handles up to 256 tokens — sufficient for individual reviews. OpenAI's text-embedding-3-large supports up to 8191 tokens for longer documents.
- **Multilingual support:** all-MiniLM-L6-v2 is English-only. A multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be needed for non-English content.
- **Accuracy vs cost:** Larger API-based models like text-embedding-3-large produce higher quality embeddings but cost money per token and require internet connectivity.
- **Latency:** Local models like all-MiniLM-L6-v2 are faster since there is no network call — important for responsive UI.

---

## Retrieval Test Results

**Query 1: "Is Erin Parker a tough grader?"**

| Result | Distance | Source | Relevant? |
|--------|----------|--------|-----------|
| 1 | 0.314 | Erin Parker, U of U, CS2100 | ✅ Yes — discusses grading style |
| 2 | 0.327 | Erin Parker, U of U, CS2420 | ✅ Yes — calls grading "arbitrary and harsh" |
| 3 | 0.335 | Erin Parker, U of U, CS2420 | ✅ Yes — "nitpicky grader" who refuses partial credit |
| 4 | 0.339 | Erin Parker, U of U, CS3810 | ✅ Yes — discusses class difficulty |
| 5 | 0.339 | Erin Parker, U of U, CS1410 | ✅ Yes — mentions high standards |

All 5 results are about Erin Parker and discuss grading. Distances well below 0.5 indicate strong semantic matches. The retrieval correctly found chunks about grading even when using different words like "nitpicky," "harsh," and "arbitrary."

**Query 2: "Which professor should I avoid at SUU?"**

| Result | Distance | Source | Relevant? |
|--------|----------|--------|-----------|
| 1 | 0.400 | Prosenjit Chatterjee, SUU | ❌ No — positive review |
| 2 | 0.411 | Nathan Barker, SUU | ❌ No — positive review |
| 3 | 0.482 | Nathan Barker, SUU | ❌ No — positive review |
| 4 | 0.486 | Aditya Bhaskara, U of U | ❌ No — wrong school |
| 5 | 0.502 | Erik Falor, Utah State | ❌ No — wrong school |

Retrieval failed here. The system found SUU professors but returned positive reviews rather than negative ones. The word "avoid" does not appear in negative reviews — students use words like "don't take" or "terrible" instead — so the semantic match found the wrong sentiment. This is the documented failure case (see below).

**Query 3: "What is Gordon Bean like as a professor?"**

| Result | Distance | Source | Relevant? |
|--------|----------|--------|-----------|
| 1 | 0.228 | Gordon Bean, BYU | ✅ Yes |
| 2 | 0.256 | Gordon Bean, BYU | ✅ Yes |
| 3 | 0.264 | Gordon Bean, BYU | ✅ Yes |
| 4 | 0.271 | Gordon Bean, BYU | ✅ Yes |
| 5 | 0.277 | Gordon Bean, BYU | ✅ Yes |

Perfect retrieval. Distances of 0.228–0.277 are the lowest observed, indicating very strong matches. Specific professor name queries produce the best retrieval results.

---

## How Grounded Generation is Enforced

Grounding is enforced through the system prompt passed to the LLM before every query. The prompt explicitly instructs the model to answer only from retrieved chunks and to refuse questions not covered by the documents:

```
You are a helpful assistant for students researching CS professors at Utah universities.

Answer the user's question using ONLY the information provided in the documents below.
Do NOT use any outside knowledge or make assumptions beyond what the documents say.
If the documents don't contain enough information to answer the question, say exactly:
'I don't have enough information in my documents to answer that question.'

Always cite which professor and school your answer draws from.
```

The retrieved chunks are passed directly in the user prompt as numbered documents. The LLM cannot reference anything outside those chunks.

---

## Example Responses

**Example 1 — Grounded response with citation (Q4: Seth Bassetti)**

*Question:* What should I know before taking Professor Seth Bassetti and what study strategies should I use?

*Response:*
> According to the documents, before taking Professor Seth Bassetti's class (CS1400) at Utah State University, you should know that his lectures can be very fast (Document 1) and sometimes may not directly align with assignment requirements (Document 3), so it's essential to stay engaged and ask questions (Document 1). The homework and assignments can take a significant amount of time each week (Documents 3 and 4), but they are considered interesting and not busywork (Document 4). His exams can be hard (Document 1), but he offers extra credit opportunities (Document 1). As for study strategies: asking questions is key to success (Document 1), being prepared to dedicate plenty of time towards weekly assignments is crucial (Document 3), and staying engaged and keeping up with the lectures is important as the pacing of the class is considered good (Document 2).

*Sources:* Seth Bassetti (Utah State University)

**Accuracy:** ✅ Accurate — matches expected answer from planning.md

---

**Example 2 — Out of scope refusal**

*Question:* What is the best restaurant near SUU campus?

*Response:*
> I don't have enough information in my documents to answer that question.

*Sources:* Vicki Allan, Nathan Barker, Prosenjit Chatterjee (retrieved but correctly ignored)

**Accuracy:** ✅ System correctly refused to hallucinate an answer not in the documents.

---

## Query Interface

**Interface type:** Gradio web UI running at http://127.0.0.1:7860

**Input fields:**
- *Your Question* — a text box where users type their question in plain language. Supports pressing Enter or clicking the Ask button to submit.

**Output fields:**
- *Answer* — the LLM-generated grounded response citing specific documents
- *Sources* — bullet list of professor names and schools the answer drew from

**Sample interaction transcript:**

```
User: Is Erin Parker a tough grader?

Answer: Yes, Erin Parker is a tough grader. This is mentioned in multiple 
documents, including Document 1, where a student mentions that she is a 
"nitpicky grader" and you will lose lots of points for skipping minor steps 
(Professor Erin Parker, University of Utah, CS2100). Similarly, Document 2 
states that her grading scheme is "arbitrary and harsh" (CS2420), and 
Document 3 notes that she is a "nitpicky grader" who may refuse partial 
credit even if an answer is almost correct (CS2420).

Sources: • Erin Parker (University of Utah)
```

---

## Evaluation Report

| # | Question | Expected Answer | System Response | Accuracy |
|---|----------|----------------|-----------------|----------|
| Q1 | Which CS professor should I avoid at SUU and why? | Hussain Aljafer — tests on untaught material, low exam averages, refuses to help | "I don't have enough information in my documents to answer that question." | ❌ Inaccurate |
| Q2 | Who is the best CS professor at BYU if you care about learning the material? | Gordon Bean — clear explanations, re-explains until everyone understands, 93% would take again | Correctly identified Gordon Bean and Cory Barker as highly praised BYU professors, with Bean specifically called "hands down best CS professor you can pick at any level" | ✅ Accurate |
| Q3 | Which CS professors should I take at University of Utah for an easy A? | None — all four are known for heavy workloads and tough grading | Said "I don't have enough information" then incorrectly mentioned Erik Falor from Utah State (wrong school) as an easy option | ⚠️ Partially accurate |
| Q4 | What should I know before taking Professor Seth Bassetti and what study strategies should I use? | Fast lectures, open note exams, start projects early, accessible office hours, ask questions | Correctly identified fast lectures, hard exams, extra credit, time-consuming assignments, and recommended asking questions and staying engaged | ✅ Accurate |
| Q5 | Based on student reviews, which CS department has the most consistently positive reviews — BYU or Utah State? | Expected partial failure | Gave a reasonable answer: BYU has more consistently positive reviews based on Gordon Bean and Cory Barker, while Utah State shows mixed reviews for Vicki Allan | ⚠️ Partially accurate |

---

## Failure Case

**Q1 — "Which CS professor should I avoid at SUU and why?"**

The system returned "I don't have enough information" despite having 13 reviews about Hussain Aljafer, many of which are strongly negative.

**Why it failed — retrieval failure caused by sentiment mismatch:**

The embedding model matched on "SUU professor" semantics but has no concept of implied negative sentiment. The word "avoid" does not appear in negative reviews — students use language like "don't take this class," "terrible professor," or "made my semester miserable." Meanwhile, positive reviews about SUU professors (Chatterjee, Nathan Barker) mention SUU prominently and scored higher cosine similarity to the query than Aljafer's negative reviews. The top 5 retrieved chunks were all positive reviews, so the LLM correctly refused to answer "who to avoid" from positive evidence — but this meant the right professor was never surfaced.

**Pipeline location:** This is a retrieval failure, not a generation failure. The LLM behaved correctly given the chunks it received. The fix would require either metadata filtering (filter by quality rating < 2.0) or hybrid search combining semantic search with keyword matching for sentiment words.

---

## Spec Reflection

**One way the spec helped:** The architecture diagram in planning.md was invaluable during implementation. Having the five stages — ingestion, chunking, embedding, retrieval, generation — clearly labeled with their tools made it obvious what to build next at every step. Rather than figuring out structure while coding, the diagram let me focus entirely on making each stage work correctly.

**One way implementation diverged from the spec:** The original planning.md did not specify using cosine similarity explicitly in ChromaDB. During testing in Milestone 4, retrieval distances came back in the 0.6–0.7 range, which the assignment flagged as weak matches. After investigation we discovered ChromaDB defaults to squared L2 distance, not cosine similarity. Adding `metadata={"hnsw:space": "cosine"}` to the collection creation dropped distances to 0.2–0.4, dramatically improving retrieval quality. This was not anticipated in the spec but was caught by the chunk inspection step the assignment required.

---

## AI Usage

**Instance 1 — Chunking and ingestion code (ingest.py):**
I prompted Claude with my Documents section, Chunking Strategy section, and a sample of my .txt file format showing the `--- REVIEWS ---` separator and blank-line-separated reviews. I asked it to implement a script that loads all 16 files and splits them into individual review chunks with metadata headers. Claude generated the `load_document()` and `chunk_reviews()` functions. I reviewed the output, ran it, and verified that chunk counts matched expected review counts per professor (e.g., Nathan Barker produced exactly 23 chunks matching his 23 reviews). I also added the 20-character minimum filter myself after noticing some very short fragments in the output.

**Instance 2 — Retrieval and generation code (embed.py and query.py):**
I prompted Claude with my Retrieval Approach section and pipeline diagram and asked it to implement the embedding step using all-MiniLM-L6-v2 and ChromaDB, plus the retrieval and generation functions. Claude generated the initial code using L2 distance. After testing showed distances above 0.6, I identified the cosine similarity issue myself and directed Claude to update the collection creation with `hnsw:space: cosine`. I also wrote and refined the grounding system prompt myself to ensure it included explicit refusal language for out-of-scope questions, which Claude's initial version did not include strongly enough.
