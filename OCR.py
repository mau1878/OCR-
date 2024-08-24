import os
import streamlit as st
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
from PIL import Image
import io
from docx import Document
import tempfile

# Function to perform OCR using Google Cloud Vision
def ocr_with_google_cloud(image_content):
    credentials = service_account.Credentials.from_service_account_file("path_to_your_google_cloud_key.json")
    client = vision.ImageAnnotatorClient(credentials=credentials)
    
    image = types.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    if not texts:
        return "No text detected."
    
    return texts[0].description

# Function to convert PDF pages to DOCX using Google Cloud OCR
def pdf_to_docx(pdf_file_path):
    doc = Document()
    pdf_document = fitz.open(pdf_file_path)
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes()))
        image_content = io.BytesIO()
        image.save(image_content, format="PNG")
        image_content = image_content.getvalue()
        
        text = ocr_with_google_cloud(image_content)
        doc.add_paragraph(text)
    
    docx_file = pdf_file_path.replace('.pdf', '.docx')
    doc.save(docx_file)
    return docx_file

# Streamlit interface
st.title("PDF to DOCX OCR Converter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    temp_dir = tempfile.mkdtemp()
    temp_pdf_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_pdf_path, "wb") as temp_pdf:
        temp_pdf.write(uploaded_file.read())

    st.write("Processing...")

    docx_file = pdf_to_docx(temp_pdf_path)

    with open(docx_file, "rb") as f:
        st.download_button("Download DOCX", f, file_name=os.path.basename(docx_file))
    
    os.remove(temp_pdf_path)
    os.remove(docx_file)
    os.rmdir(temp_dir)

st.write("Upload a PDF file to convert it into a DOCX file using OCR.")
