from PyPDF2 import PdfReader

def pdf_converter(doc):
    cdoc = PdfReader(doc)
    edoc =""

    for page in cdoc.pages:
        edoc += page.extract_text()

    return edoc