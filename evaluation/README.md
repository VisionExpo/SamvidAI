# 📊 SamvidAI – Evaluation Framework

This directory contains the **evaluation methodology, baselines, and evidence artifacts**
used to track SamvidAI’s **system-level improvements over time**.

The goal of evaluation in SamvidAI is **engineering confidence**, not artificial accuracy scores.

SamvidAI is a retrieval-augmented, LLM-assisted legal system where correctness depends on:
- Deterministic pipelines (retrieval, scoring, aggregation)
- Probabilistic reasoning (LLM explanations)

Accordingly, evaluation is **structured, versioned, and evidence-driven**.

---

## 🎯 Evaluation Objectives

The evaluation framework is designed to:

- Measure **system stability and regressions**
- Track **performance improvements across versions**
- Validate **retrieval and risk pipeline consistency**
- Provide **concrete artifacts** to demonstrate progress to reviewers and recruiters

> We prioritize *repeatability, explainability, and trend analysis* over brittle accuracy metrics.

---

## 🗂️ Directory Structure

```

evaluation/
├── golden_docs/     # Frozen evaluation documents (never change)
├── baselines/       # Versioned reference metrics (v0.1.0, v0.2.0, ...)
├── runs/            # Time-stamped evaluation runs
├── reports/         # Human-readable analysis & trend summaries
└── README.md        # This document

```

---

## 📌 Golden Documents

Golden documents are **fixed reference PDFs** used across all evaluation runs.
They represent different legal genres and complexity levels.

| Document | Category | Purpose |
|--------|--------|--------|
| Arbitration & Conciliation Act, 1996 | Statute | Long-form legal retrieval grounding |
| Indian Contract Act, 1872 | Statute | Structural legal reasoning |
| BARC General Conditions of Contract | Govt Contract | Clause-level risk analysis |
| Amazon vs Future Retail (2020) | Judgment | Long-document performance stress |
| NDA (Synthetic) | Synthetic | Controlled regression testing |

Golden documents **must never be modified** to ensure fair comparisons across versions.

---

## 📈 Metrics Tracked

### 1️⃣ Performance Metrics (Deterministic)

- End-to-end latency (p50 / p95)
- Retrieval latency
- Token usage per request
- Token reduction vs full-document prompting
- Memory (CPU / VRAM where applicable)

### 2️⃣ Retrieval Stability

- Top-K result count consistency
- Empty retrieval rate
- Embedding dimensional stability
- Vector store query safety

### 3️⃣ Risk Engine Consistency

- Clause risk label distribution
- Risk score variance
- Score boundary adherence
- Aggregation determinism

> LLM-generated explanations are **not linguistically asserted**.

---

## 🔁 Versioned Baselines

Each stable milestone introduces a **baseline snapshot**:

```

evaluation/baselines/
├── v0.1.0.json
├── v0.2.0.json
└── v0.3.0.json

```

Baselines capture:
- Performance metrics
- Retrieval shape statistics
- Risk score distributions

They serve as **reference points** for regression detection.

---

## 🧪 Evaluation Runs

Evaluation runs are **time-stamped executions** of the pipeline on golden documents.

```

evaluation/runs/
├── 2026-02-01.json
├── 2026-02-05.json
└── latest.json

```

Each run records:
- Commit hash
- System version
- Environment metadata
- Measured metrics

Runs are compared **against the most recent baseline**, not arbitrary thresholds.

---

## 📉 Regression Signals

A regression is flagged when one or more of the following occurs:

- Latency increase > 30%
- Token usage deviation outside expected bounds
- Retrieval output shape change
- Risk score drift beyond tolerated variance
- Memory usage spike

Regression analysis is documented in `/evaluation/reports/`.

---

## 🧾 Reports & Evidence

Human-readable summaries live in:

```

evaluation/reports/

```

Examples:
- Latency trend analysis
- Retrieval stability review
- Risk score drift analysis

Visual artifacts (charts, plots) are stored in:

```

assets/
├── latency_plots/
├── memory_profiles/
└── charts/

```

---

## 🧠 What We Do NOT Measure (Intentionally)

- Exact LLM phrasing
- Subjective legal correctness
- Creative language quality
- UI visual accuracy

These are evaluated via:
- Human review
- Qualitative analysis
- Domain expertise

---