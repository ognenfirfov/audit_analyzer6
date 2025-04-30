import openai
import fitz  # PyMuPDF
import pandas as pd
import os

# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_ai_to_summarize(text):
    """Sends the extracted PDF text to OpenAI and returns structured insights."""
    prompt = f"""You are an audit report analyzer. Given the following audit report, extract the following:
- Main Audit Topic
- Main Findings
- Measures Taken
- Recommended Next Steps

Report:
{text}

Return in this format:
Main Audit Topic: ...
Main Findings: ...
Measures Taken: ...
Next Steps: ...
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0]["message"]["content"]

def process_audits(file_paths):
    """Processes a list of PDF file paths and returns a comparison table."""
    data = []
    for i, path in enumerate(file_paths):
        text = extract_text_from_pdf(path)
        summary = ask_ai_to_summarize(text)

        # Parse AI output into a structured format
        summary_lines = summary.splitlines()
        parsed = {"Company": f"Audit {i+1}"}
        for line in summary_lines:
            if ":" in line:
                key, val = line.split(":", 1)
                parsed[key.strip()] = val.strip()
        data.append(parsed)

    return pd.DataFrame(data)
