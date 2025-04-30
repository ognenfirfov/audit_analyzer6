
import streamlit as st
from utils.audit_parser import process_audits
import tempfile
import os

st.set_page_config(page_title="Audit Analyzer", layout="wide")
st.title("📊 Audit Analyzer")
st.markdown("Upload 3–4 PDF audit reports of **similar companies** to extract and compare key conclusions.")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) < 3 or len(uploaded_files) > 4:
        st.warning("Please upload between 3 and 4 PDF files.")
    else:
        with st.spinner("Analyzing audit reports with AI..."):
            # Save uploaded files temporarily
            temp_paths = []
            for file in uploaded_files:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                temp_file.write(file.read())
                temp_paths.append(temp_file.name)

            table_data = process_audits(temp_paths)

            st.success("Analysis complete!")
            st.markdown("### 🧾 Audit Comparison Table")
            st.dataframe(table_data, use_container_width=True)

            # Clean up
            for path in temp_paths:
                os.remove(path)
