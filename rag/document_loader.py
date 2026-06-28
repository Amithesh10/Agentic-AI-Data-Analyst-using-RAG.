from pypdf import PdfReader
from docx import Document


def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def read_docx(file):
    doc = Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")


def load_document(file):
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return read_pdf(file)

    elif file_name.endswith(".docx"):
        return read_docx(file)

    elif file_name.endswith(".txt"):
        return read_txt(file)

    else:
        return ""