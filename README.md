# 🧠 LegalLens  
## Intelligent Contract Analysis Engine powered by OpticalRAG

LegalLens is a next-generation **legal document intelligence platform** designed to analyze long, complex legal contracts (100+ pages) with **layout awareness, low latency, and human-in-the-loop validation**.

Unlike traditional OCR or text-only NLP pipelines that flatten documents and lose structure, LegalLens introduces **OpticalRAG** — a visual-first, retrieval-augmented architecture that preserves spatial context while dramatically reducing token cost, latency, and hallucinations.

> **Philosophy**  
> *We do not replace attorneys. We empower them.*  
> LegalLens automates extraction, risk flagging, and summarization so legal experts can focus on judgment, validation, and strategy.

---

## 🚀 Why LegalLens?

### ❌ The Problem

Legal contracts are:
- Extremely **long and repetitive**
- Highly **structured and visual**
- Filled with **risk-sensitive clauses**

Traditional systems fail because:

- OCR-based pipelines destroy:
  - Tables
  - Multi-column layouts
  - Clause hierarchy
- Feeding entire contracts into LLMs is:
  - Expensive
  - Slow
  - Prone to *lost-in-the-middle* hallucinations
- Pure text RAG ignores layout and spatial semantics

---

### ✅ The Solution

LegalLens uses **OpticalRAG**, a hybrid **vision + retrieval + LLM** system that:

- Treats contract pages as **visual data**
- Retrieves **only relevant regions**
- Converts to text **only when required**

**Results**
- ✅ Lower inference cost  
- ✅ Higher accuracy  
- ✅ Layout-aware reasoning  
- ✅ Scales to 100+ page contracts  

---

## 🧠 OpticalRAG Architecture

Traditional RAG pipelines fail on massive legal documents due to lossy OCR and limited context windows.

**OpticalRAG solves this by design.**

### 🔁 End-to-End Pipeline
```
PDF Contract
↓
High-Resolution Page Images (300 DPI)
↓
Layout-Aware Segmentation (LayoutLMv3)
↓
Semantic Regions (Clauses, Tables, Headers)
↓
Multimodal Embeddings (Text + Vision)
↓
Vector Retrieval (Query-Aware)
↓
LLM Reasoning on Relevant Regions Only
```

### 🧩 Why OpticalRAG Works

- Preserves **spatial and structural context**
- Avoids full-document text ingestion
- Mitigates hallucinations
- Reduces token usage and latency
- Enables clause-level reasoning

---

## 🧩 Core Features

### 🔍 OpticalRAG Retrieval
- Vision-first document understanding
- Multimodal embeddings (text + layout)
- Hierarchical retrieval:
  - Page → Section → Clause
- Query-aware region selection

---

### ⚠️ Automated Risk Detection
Automatically flags:
- One-sided obligations
- Non-standard clauses
- Missing or weak protections
- Compliance risks

**Risk Levels**
- 🔴 High Risk
- 🟠 Needs Review
- 🟢 Standard

---

### 📊 Predictive Clause Analytics
- Identifies clauses historically linked to disputes
- Highlights friction-prone contract sections
- Supports proactive risk mitigation

---

### 📝 Smart Summarization
Generates role-specific summaries:
- Executive Summary
- Financial Liabilities
- Technical Constraints
- Legal Obligations

---

### 👨‍⚖️ Human-in-the-Loop Review
- Attorneys can:
  - Accept AI flags
  - Reject incorrect findings
  - Edit interpretations
- Feedback enables:
  - Active learning
  - Dataset creation
  - Continuous improvement
- Creates a **long-term legal intelligence moat**

---

## 🛠️ Tech Stack (Open-Source First)

### 🧱 Core
- **Python 3.10+**
- **FastAPI** – backend APIs
- **Streamlit** – MVP review dashboard

---

### 👁️ Vision & Layout
- **LayoutLMv3** – layout-aware document understanding
- **PaddleOCR** – auxiliary text extraction

---

### 🧠 Embeddings & Retrieval
- **OpenCLIP (ViT-H/14)** – multimodal embeddings
- **BGE / E5** – legal text embeddings
- **ChromaDB** – local vector store (Pinecone-ready)

---

### 🤖 LLMs (Local-Friendly)
- **Qwen2.5-7B-Instruct**
- **Mistral 7B Instruct**
- **Phi-3 Medium**

> Optimized for consumer GPUs (RTX 4060, 8 GB VRAM) using quantization.

---

## 📂 Project Structure
```
LegalLens/
├── core/
│ ├── ingestion/ # PDF → image pipelines
│ ├── layout/ # Layout-aware segmentation
│ ├── retrieval/ # OpticalRAG logic
│ └── risk_engine/ # Clause classification & risk scoring
├── models/
│ ├── embeddings/
│ └── llm/
├── api/
│ └── main.py # FastAPI endpoints
├── ui/
│ └── streamlit_app.py # Human-in-the-loop dashboard
├── data/
│ ├── raw/
│ └── processed/
├── tests/
├── docker/
│ └── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🧪 Research Techniques Used

LegalLens incorporates modern retrieval and LLM research, including:

- Hierarchical RAG
- Query-aware retrieval
- Late chunking
- Lost-in-the-middle mitigation
- Contrastive multimodal embeddings
- Hybrid rule-based + LLM reasoning
- Human-in-the-loop active learning

---

## 🗺️ Roadmap

### Phase 1 — Ingestion Pipeline
- [ ] PDF → image conversion
- [ ] Layout-aware region extraction
- [ ] Multimodal embeddings

### Phase 2 — OpticalRAG Core
- [ ] Query-based visual retrieval
- [ ] Clause-level reasoning

### Phase 3 — Risk Engine
- [ ] Clause classification
- [ ] Red / Amber / Green scoring

### Phase 4 — Review Interface
- [ ] Attorney validation UI
- [ ] Feedback capture

### Phase 5 — Optimization
- [ ] Latency tuning for long contracts
- [ ] Model quantization
- [ ] Dataset-driven improvements

---

## 🎯 Vision

LegalLens is built with a **startup-first mindset**:

- Solves a real legal pain point
- Optimized for limited hardware
- Open-source friendly
- Enterprise-ready foundation

The long-term goal is to evolve LegalLens into a **full legal intelligence platform** for contract review, compliance, and dispute risk forecasting.

---

## 🤝 Contributing

Contributions, ideas, and discussions are welcome.

If you're interested in:
- Legal AI
- Multimodal RAG
- Human-in-the-loop systems

You’ll feel right at home here.

---

## 📜 License

MIT License
