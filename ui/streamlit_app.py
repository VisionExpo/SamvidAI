import sys
import os
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ui.api_client import analyze_contract


st.set_page_config(page_title="SamvidAI", layout="wide")

st.title("🧠 SamvidAI – Contract Risk Analyzer")

# PDF Path input
pdf_path = st.text_input(
    "Contract PDF Path",
    placeholder="data/govt_contracts/BARC_General_Conditions_of_Contract_GCC.pdf",
    help="Enter the full path to the contract PDF file"
)

# Top K slider
top_k = st.slider("Number of clauses to analyze", min_value=5, max_value=20, value=10)

if st.button("Analyze Contract"):
    if not pdf_path.strip():
        st.warning("Please enter a PDF path.")
    else:
        with st.spinner("Analyzing contract..."):
            try:
                result = analyze_contract(pdf_path, top_k=top_k)

                # Display metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Level", result["risk_level"])
                col2.metric("Risk Score", result["risk_score"])
                col3.metric("Clauses Analyzed", result["clauses_analyzed"])

                # Display clause-level details
                st.subheader("📋 Clause Analysis")
                
                if result.get("clauses"):
                    for clause in result["clauses"]:
                        with st.expander(f"Clause: {clause['clause_id']} - {clause['risk_level']} Risk"):
                            st.markdown(f"**Text:** {clause['text']}")
                            st.markdown(f"**Risk Level:** {clause['risk_level']}")
                            st.markdown(f"**Reason:** {clause['reason']}")
                else:
                    st.info("No risky clauses detected.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the backend is running and the PDF path is correct.")
