import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from docx import Document
import tempfile
import os

# Function to perform OCR on a PDF and save as DOCX
def pdf_to_docx(pdf_file):
    # Convert PDF to images
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_file, output_folder=path, fmt='png')
    
        # Create a new DOCX document
        doc = Document()
        
        for image in images:
            # Perform OCR on each image
            text = pytesseract.image_to_string(image)
            doc.add_paragraph(text)
        
        # Save the DOCX file
        docx_file = pdf_file.replace('.pdf', '.docx')
        doc.save(docx_file)
        return docx_file

# Streamlit interface
st.title("PDF to DOCX OCR Converter")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name
    
    st.write("Processing...")
    
    # Perform OCR and convert to DOCX
    docx_file = pdf_to_docx(temp_pdf_path)
    
    # Provide a download link for the DOCX file
    with open(docx_file, "rb") as f:
        st.download_button("Download DOCX", f, file_name=os.path.basename(docx_file))
    
    # Cleanup temporary files
    os.remove(temp_pdf_path)
    os.remove(docx_file)

st.write("Upload a PDF file to convert it into a DOCX file using OCR.")
