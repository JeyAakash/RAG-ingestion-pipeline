# rag_project.py
import os
import docx

print("=== RAG DYNAMIC PARSING & CHUNKING PIPELINE (DOCX VERSION) ===\n")

# -------------------------------------------------------------------------
# Step 1: Dynamic File Loading (Scans workspace for .docx files)
# -------------------------------------------------------------------------
def load_docx_documents(folder_path="."):
    """Scans the workspace directory for Word documents to ingest."""
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            doc = docx.Document(file_path)
            # Extract all paragraphs and join them into full text
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            documents[filename] = full_text
    return documents

corpus = load_docx_documents()
print(f"-> Loaded {len(corpus)} document(s) from workspace: {list(corpus.keys())}\n")

# -------------------------------------------------------------------------
# Step 2: Strategy A - Fixed-Size Baseline Chunker
# -------------------------------------------------------------------------
def fixed_size_chunker(text, chunk_size=180):
    """Strategy A: Blindly splits text into rigid chunks."""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk_text = text[i:i + chunk_size].strip()
        if chunk_text:
            chunks.append({
                "strategy": "fixed_size",
                "text": chunk_text
            })
    return chunks

# -------------------------------------------------------------------------
# Step 3: Strategy B - Dynamic Structure-Aware Chunker with Metadata
# -------------------------------------------------------------------------
def dynamic_structure_chunker(text, source_id="policy.docx"):
    """Strategy B: Structure-aware chunking preserving context and sections."""
    sections = text.split("Section ")
    chunks = []
    
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        section_title = "Section " + lines[0]
        section_body = "\n".join(lines[1:])
        
        chunks.append({
            "strategy": "dynamic_structure",
            "metadata": {
                "source_id": source_id,
                "section_path": f"Root > {section_title}"
            },
            "text": section_body.strip()
        })
        
    return chunks

# -------------------------------------------------------------------------
# Step 4: Execute Ingestion Pipeline
# -------------------------------------------------------------------------
all_fixed_chunks = []
all_dynamic_chunks = []

for filename, content in corpus.items():
    print(f"Processing '{filename}' through chunkers...")
    all_fixed_chunks.extend(fixed_size_chunker(content))
    all_dynamic_chunks.extend(dynamic_structure_chunker(content, source_id=filename))

print(f"\n-> Total Chunks Produced:")
print(f"   - Fixed-Size Chunks: {len(all_fixed_chunks)}")
print(f"   - Dynamic Structure Chunks: {len(all_dynamic_chunks)}\n")

# -------------------------------------------------------------------------
# Step 5: Quantitative Evaluation & Comparison
# -------------------------------------------------------------------------
def run_evaluation(chunks_list, query, target_keyword):
    """Evaluates whether the retriever successfully captures complete context."""
    matched = [c for c in chunks_list if target_keyword.lower() in c["text"].lower()]
    
    print(f"Query: '{query}'")
    if matched:
        print(f"   Status: SUCCESS (Found match using strategy: {matched[0]['strategy']})")
        print(f"   Retrieved Text Snippet:\n   {matched[0]['text'][:250]}...\n")
    else:
        print("   Status: FAILED (Context was broken or missing!)\n")

test_query = "What happens if an employee cannot access their work email?"
keyword = "identity team must manually verify"

print("--- Testing Strategy A (Fixed-Size Chunker) ---")
run_evaluation(all_fixed_chunks, test_query, keyword)

print("--- Testing Strategy B (Dynamic Structure Chunker) ---")
run_evaluation(all_dynamic_chunks, test_query, keyword)