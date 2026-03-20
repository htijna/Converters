import os
import uuid
import fitz  # PyMuPDF
from PIL import Image
from pdf2docx import Converter
import traceback

# Fallback imports
try:
    print("Attempting to import aspose.words...")
    import aspose.words as aw
    print("aspose.words imported successfully.")
except Exception as e:
    print(f"aspose.words import failed: {e}")
    aw = None

try:
    print("Attempting to import aspose.slides...")
    import aspose.slides as asv
    print("aspose.slides imported successfully.")
except Exception as e:
    print(f"aspose.slides import failed: {e}")
    asv = None

try:
    from docx2pdf import convert as docx_to_pdf_win
except ImportError:
    docx_to_pdf_win = None

try:
    import comtypes.client
except ImportError:
    comtypes_client = None

class FileConverter:
    @staticmethod
    def pdf_to_docx(input_path, output_path):
        try:
            print(f"Starting PDF to DOCX: {input_path} -> {output_path}")
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            print("PDF to DOCX successful.")
            return True
        except Exception as e:
            print(f"PDF to DOCX Error: {e}")
            traceback.print_exc()
            raise e

    @staticmethod
    def docx_to_pdf(input_path, output_path):
        print(f"Starting DOCX to PDF: {input_path} -> {output_path}")
        # Try docx2pdf first (requires Word, but no watermark)
        if docx_to_pdf_win:
            try:
                print("Trying docx2pdf...")
                docx_to_pdf_win(input_path, output_path)
                print("docx2pdf successful.")
                return True
            except Exception as e:
                print(f"docx2pdf failed: {e}")
        
        # Fallback to Aspose
        if aw:
            try:
                print("Trying aspose.words...")
                doc = aw.Document(input_path)
                doc.save(output_path)
                print("aspose.words successful.")
                return True
            except Exception as e:
                print(f"aspose.words failed: {e}")
        
        raise Exception("No Word to PDF backend available or it failed.")

    @staticmethod
    def pptx_to_pdf(input_path, output_path):
        print(f"Starting PPTX to PDF: {input_path} -> {output_path}")
        # Try comtypes first (requires PowerPoint)
        if comtypes_client:
            try:
                print("Trying comtypes (PowerPoint)...")
                powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
                powerpoint.Visible = 1
                pres = powerpoint.Presentations.Open(os.path.abspath(input_path))
                # 32 is ppSaveAsPDF
                pres.SaveAs(os.path.abspath(output_path), 32)
                pres.Close()
                powerpoint.Quit()
                print("comtypes (PowerPoint) successful.")
                return True
            except Exception as e:
                print(f"comtypes failed: {e}")

        # Fallback to Aspose
        if asv:
            try:
                print("Trying aspose.slides...")
                pres = asv.Presentation(input_path)
                pres.save(output_path, asv.export.SaveFormat.PDF)
                print("aspose.slides successful.")
                return True
            except Exception as e:
                print(f"aspose.slides failed: {e}")

        raise Exception("No PPT to PDF backend available.")

    @staticmethod
    def pdf_to_image(input_path, output_path):
        try:
            print(f"Starting PDF to Image: {input_path} -> {output_path}")
            doc = fitz.open(input_path)
            if len(doc) > 0:
                page = doc.load_page(0)
                pix = page.get_pixmap()
                pix.save(output_path)
                doc.close()
                print("PDF to Image successful.")
                return True
            doc.close()
            return False
        except Exception as e:
            print(f"PDF to Image Error: {e}")
            raise e

    @staticmethod
    def image_to_pdf(input_path, output_path):
        try:
            print(f"Starting Image to PDF: {input_path} -> {output_path}")
            image = Image.open(input_path)
            image.convert("RGB").save(output_path, "PDF")
            print("Image to PDF successful.")
            return True
        except Exception as e:
            print(f"Image to PDF Error: {e}")
            raise e

    @staticmethod
    def get_converter(file_ext, target_format):
        converters = {
            ("pdf", "docx"): FileConverter.pdf_to_docx,
            ("docx", "pdf"): FileConverter.docx_to_pdf,
            ("pptx", "pdf"): FileConverter.pptx_to_pdf,
            ("pdf", "jpg"): FileConverter.pdf_to_image,
            ("pdf", "png"): FileConverter.pdf_to_image,
            ("jpg", "pdf"): FileConverter.image_to_pdf,
            ("png", "pdf"): FileConverter.image_to_pdf,
            ("jpeg", "pdf"): FileConverter.image_to_pdf,
        }
        return converters.get((file_ext, target_format))
