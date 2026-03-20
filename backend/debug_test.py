import os
import sys
from services.converter import FileConverter
from docx import Document
from pptx import Presentation

def test_all():
    print("--- TESTING CONVERTERS ---")
    
    # 1. Image to PDF
    print("\n1. Testing Image to PDF...")
    from PIL import Image
    test_img = "test_input.jpg"
    Image.new('RGB', (100, 100), color='red').save(test_img)
    try:
        FileConverter.image_to_pdf(test_img, "test_output.pdf")
        print("SUCCESS: Image to PDF")
    except Exception as e:
        print(f"FAILED: Image to PDF: {e}")

    # 2. DOCX to PDF
    print("\n2. Testing DOCX to PDF...")
    test_docx = "test_input.docx"
    doc = Document()
    doc.add_paragraph("Test")
    doc.save(test_docx)
    try:
        FileConverter.docx_to_pdf(test_docx, "test_docx_output.pdf")
        print("SUCCESS: DOCX to PDF")
    except Exception as e:
        print(f"FAILED: DOCX to PDF: {e}")

    # 3. PDF to DOCX
    print("\n3. Testing PDF to DOCX...")
    try:
        if os.path.exists("test_docx_output.pdf"):
            FileConverter.pdf_to_docx("test_docx_output.pdf", "test_docx_result.docx")
            print("SUCCESS: PDF to DOCX")
        else:
            print("SKIPPED: PDF to DOCX (no input PDF)")
    except Exception as e:
        print(f"FAILED: PDF to DOCX: {e}")

    # Cleanup
    for f in ["test_input.jpg", "test_output.pdf", "test_input.docx", "test_docx_output.pdf", "test_docx_result.docx"]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

if __name__ == "__main__":
    test_all()
