# RAG Ingestion Pipeline: Dynamic Parsing & Structure-Aware Chunking

An advanced Retrieval-Augmented Generation (RAG) ingestion pipeline built in Python. This project compares traditional **Fixed-Size Chunking (Strategy A)** against **Dynamic Structure-Aware Chunking (Strategy B)** using local Word (`.docx`) documents to evaluate context completeness and retrieval accuracy.

---

## 🚀 Project Overview
In standard RAG systems, blindly splitting documents into rigid, fixed-size chunks often severs critical context—such as separating security rules from their corresponding exceptions or cutting tables mid-row. 

This project demonstrates how **Dynamic Structure-Aware Parsing** preserves document hierarchy (`Root > Section`), serializes table headers to values, and ensures complete context windows for Large Language Models (LLMs).

---

## 📂 Project Structure
```text
rag-ingestion-project/
│
├── rag_project.py                         # Main ingestion, chunking, and evaluation script
├── Employee_Expense_and_Support_Policy.docx # Sample corporate policy document
└── README.md                              # Project documentation
