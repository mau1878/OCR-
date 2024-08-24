import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from docx import Document
from PIL import Image
import io
import tempfile
import os

# Function to perform OCR on a PDF and save as DOCX
def pdf_to_docx(pdf_file_path):
    doc = Document()
    pdf_document = fitz.open(pdf_file_path)
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes()))
        text = pytesseract.image_to_string(image)
        doc.add_paragraph(text)
    
    docx_file = pdf_file_path.replace('.pdf', '.docx')
    doc.save(docx_file)
    return docx_file

# Streamlit interface
st.title("PDF to DOCX OCR Converter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Save the uploaded file to the temp directory
    temp_pdf_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_pdf_path, "wb") as temp_pdf:
        temp_pdf.write(uploaded_file.read())

    st.write("Processing...")
    
    # Perform OCR and convert to DOCX
    docx_file = pdf_to_docx(temp_pdf_path)

    # Provide a download link for the DOCX file
    with open(docx_file, "rb") as f:
        st.download_button("Download DOCX", f, file_name=os.path.basename(docx_file))
    
    # Cleanup: remove the temporary files and directory
    os.remove(temp_pdf_path)
    os.remove(docx_file)
    os.rmdir(temp_dir)

st.write("Upload a PDF file to convert it into a DOCX file using OCR.")
