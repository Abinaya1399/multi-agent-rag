import requests
from pypdf import PdfReader

def load_pdf_from_url(url):
    response = requests.get(url)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    reader = PdfReader("temp.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
