# 🧪 Testing Strategy & Plan

This document outlines the **testing philosophy, scope, and roadmap** for SamvidAI, aligned with the current test suite structure.

SamvidAI is a **multimodal, retrieval-augmented AI system**, where correctness depends on both deterministic pipelines and probabilistic model behavior.
Testing is therefore **layered, pragmatic, and staged**, focusing on stability, regressions, and system confidence rather than brittle assertions.

---

## 🎯 Testing Philosophy

* Test **what can deterministically fail**
* Avoid over-asserting probabilistic LLM outputs
* Prioritize **pipeline stability, regressions, and safety**
* Introduce strict tests **only after behavior stabilizes**

> The goal is confidence and safety — not 100% coverage.

---

## 🧱 Testing Layers & Mapping

| Layer            | Purpose                            | Test Paths                          |
| ---------------- | ---------------------------------- | ----------------------------------- |
| API Tests        | Contract stability & schema safety | `tests/api/`                        |
| Pipeline Tests   | Deterministic transformations      | `tests/layout/`, `tests/retrieval/` |
| Logic Tests      | Rule-based correctness             | `tests/risk_engine/`                |
| LLM Safety Tests | Prompt & guardrail safety          | `tests/llm/`                        |
| Dependency Tests | Injection & wiring                 | `tests/injection/`                  |

---

## 🧪 Test Suite Breakdown (By Path)

### 1️⃣ API Layer

**Path:** `tests/api/`

Files:

* `test_health.py`
* `test_analyze_contract.py`

**Focus:**

* Endpoint availability
* Request/response schema validation
* Failure handling (bad input, empty files)

**Explicitly NOT tested:**

* Semantic correctness of LLM output

---

### 2️⃣ Dependency Injection & Wiring

**Path:** `tests/injection/test_deps.py`

**Focus:**

* Dependency graph resolution
* Mock vs production dependency switching
* Startup failure prevention

Goal: ensure the system **boots predictably** in all environments.

---

### 3️⃣ Layout & Document Segmentation

**Path:** `tests/layout/test_layout_segmentation.py`

**Focus:**

* Page & block segmentation
* Layout object consistency
* Failure safety on malformed documents

Validated properties:

* Non-empty outputs
* Stable bounding boxes
* Deterministic segmentation behavior

---

### 4️⃣ Retrieval & Embeddings

**Path:** `tests/retrieval/test_retriever.py`

**Focus:**

* Embedding pipeline stability
* Vector store insert/query safety
* Top-K retrieval shape consistency

Notes:

* Retrieval relevance is validated **manually** during early stages
* Tests ensure **numerical and structural correctness**, not semantic quality

---

### 5️⃣ Risk Engine

**Path:** `tests/risk_engine/`

Files:

* `test_classifier.py`
* `test_scorer.py`

**Focus:**

* Clause → category mapping
* Risk score boundaries
* Deterministic label assignment (Red / Amber / Green)

LLM-generated explanations are **not strictly asserted**.

---

### 6️⃣ LLM Safety & Prompting

**Path:** `tests/llm/`

Files:

* `test_guardrails.py`
* `test_prompts.py`

**Focus:**

* Prompt template stability
* Guardrail enforcement
* Prevention of prompt injection & runaway outputs

Assertions are **structural and policy-based**, not linguistic.

---

## 🔁 Regression Testing Strategy

Regression tests are introduced **after acceptable behavior is observed**.

Regression signals include:

* Latency increase > 30%
* Token usage deviation
* Retrieval output shape changes
* Risk score drift outside thresholds

---

## ⚙️ Performance & Resource Awareness

Performance testing is **first-class**, even if lightweight initially.

Tracked signals:

* End-to-end latency
* Token usage per request
* VRAM & CPU memory usage

Target benchmarks:

* < 15s for 120-page contract
* VRAM < 8 GB
* ≥ 60% token reduction vs full-text RAG

---

## 🧠 What We Intentionally Do NOT Test Early

* Exact LLM phrasing
* Subjective legal correctness
* UI pixel-perfect rendering
* Creative language quality

These are validated via:

* Human review
* Qualitative evaluation
* Data & evaluation reports

---

## 🛠️ Tools & Execution

* `pytest` for unit & integration tests
* Controlled fixtures & mocks
* Logging-based assertions for performance

CI will be enabled once:

* Pipelines stabilize
* Test outcomes are deterministic

---

## 🧭 Final Note

Testing in SamvidAI is **intentional, safety-oriented, and staged**.

The strategy favors:

* Stability over premature rigor
* Guardrails over fragile correctness
* Human-validated intelligence over brittle tests

This approach ensures confidence **without slowing down innovation**.
