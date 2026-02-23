import sys
import os
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ui.api_client import analyze_contract_from_upload


st.set_page_config(page_title="SamvidAI", layout="wide")

st.title("🧠 SamvidAI – Contract Risk Analyzer")

# PDF File uploader
uploaded_file = st.file_uploader(
    "Upload Contract PDF",
    type=["pdf"],
    help="Upload a contract PDF file to analyze"
)

# Data source selection
data_source = st.selectbox(
    "Data Source",
    options=["govt_contracts", "synthetic_contracts", "public_judgments", "acts_and_rules"],
    help="Select where to store the uploaded contract"
)

# Top K slider
top_k = st.slider("Number of clauses to analyze", min_value=5, max_value=20, value=10)

if st.button("Analyze Contract"):
    if uploaded_file is None:
        st.warning("Please upload a PDF file.")
    else:
        with st.spinner("Analyzing contract..."):
            try:
                # Read the file content
                file_content = uploaded_file.getvalue()
                filename = uploaded_file.name
                
                result = analyze_contract_from_upload(
                    file_content, 
                    filename, 
                    top_k=top_k,
                    data_source=data_source
                )

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
                st.info("Make sure the backend is running and the PDF file is valid.")
