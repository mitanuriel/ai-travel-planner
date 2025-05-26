import PyPDF2

def extract_text_from_pdf(file):
    """Extracts text from an uploaded PDF file object."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_txt(file):
    """Extracts text from an uploaded TXT file object."""
    content = file.read()
    # Handle both bytes and string (for Streamlit)
    if isinstance(content, bytes):
        return content.decode("utf-8", errors="ignore")
    return content
