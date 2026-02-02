import streamlit as st
import requests
from pathlib import Path

def risk_level(score: int) -> str:
    if score >= 2:
        return "HIGH"
    if score == 1:
        return "MEDIUM"
    return "LOW"


def risk_color(level: str) -> str:
    return {
        "HIGH": "🔴",
        "MEDIUM": "🟠",
        "LOW": "🟢",
    }[level]

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="SamvidAI", layout="wide")
st.title("🧠 SamvidAI — Contract Analysis")

st.markdown("Upload a contract and ask a legal question.")

# --- Upload ---
uploaded_file = st.file_uploader("Upload contract PDF", type=["pdf"])

question = st.text_input("Legal question", placeholder="e.g. What are the termination conditions?")

analyze = st.button("Analyze Contract")

if analyze:
    if not uploaded_file or not question:
        st.warning("Please upload a PDF and enter a question.")

    else:
        # Save uploaded file locally (Only for demo)
        data_dir = Path("data/ui_uploads")
        data_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = data_dir / uploaded_file.name

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        payload = {
            "pdf_path": str(pdf_path),
            "question": question,
        }

        # --- Risk Analysis ---
        with st.spinner("Analyzing risks..."):
            risk_resp = requests.post(
                f"{API_URL}/analyze-risk",
                json=payload,
                timeout=300,
            )

        if risk_resp.status_code == 200:
            risks = risk_resp.json()["risks"]

            st.subheader("⚠️ Risk Analysis")

            if not risks:
                st.success("No significant risks detected.")
            else:
                for r in risks:
                    level = risk_level(r["risk_score"])
                    color = risk_color(level)

                    with st.expander(f"{color} {level} — {r['clause_id']}"):
                        if r["risks"]:
                            for item in r["risks"]:
                                st.write(f"- {item}")
                        else:
                            st.write("No explicit risks detected.")