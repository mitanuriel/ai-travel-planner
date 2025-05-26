import PyPDF2
import re

def extract_text_from_pdf(file):
    """Extracts text from an uploaded PDF file object and cleans up spaces."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"   # <-- This line should be inside the loop, but no extra indent!
    
    # Clean up text: Replace multiple spaces/newlines with a single one
    text = re.sub(r'\n+', '\n', text)         # Collapse multiple newlines
    text = re.sub(r'[ ]{2,}', ' ', text)      # Collapse multiple spaces
    return text.strip()


def extract_text_from_txt(file):
    """Extracts text from an uploaded TXT file object."""
    content = file.read()
    # Handle both bytes and string (for Streamlit)
    if isinstance(content, bytes):
        return content.decode("utf-8", errors="ignore")
    return content
