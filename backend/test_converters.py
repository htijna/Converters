import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

results = []

# 1. Check imports
results.append("=== IMPORT STATUS ===")

modules = {
    "fitz (PyMuPDF)": "import fitz",
    "Pillow": "from PIL import Image", 
    "pdf2docx": "from pdf2docx import Converter",
    "aspose.words": "import aspose.words",
    "aspose.slides": "import aspose.slides",
    "docx2pdf": "from docx2pdf import convert",
    "comtypes": "import comtypes.client",
}

for name, stmt in modules.items():
    try:
        exec(stmt)
        results.append(f"  OK: {name}")
    except Exception as e:
        results.append(f"  FAIL: {name} -> {e}")

# 2. Check which conversion paths are available
results.append("\n=== CONVERSION PATHS ===")

from services.converter import FileConverter

test_pairs = [
    ("pdf", "docx", "PDF -> Word"),
    ("docx", "pdf", "Word -> PDF"),
    ("pptx", "pdf", "PPT -> PDF"),
    ("pdf", "png", "PDF -> Image"),
    ("jpg", "pdf", "Image -> PDF"),
]

for src, tgt, label in test_pairs:
    conv = FileConverter.get_converter(src, tgt)
    results.append(f"  {'OK' if conv else 'MISSING'}: {label} ({src} -> {tgt})")

# 3. Quick functional tests
results.append("\n=== FUNCTIONAL TESTS ===")

base = os.path.dirname(os.path.abspath(__file__))
test_pdf = os.path.join(base, "test.pdf")
test_docx = os.path.join(base, "test.docx")

# PDF -> PNG
if os.path.exists(test_pdf):
    out = os.path.join(base, "_diag_out.png")
    try:
        FileConverter.pdf_to_image(test_pdf, out)
        sz = os.path.getsize(out)
        results.append(f"  OK: PDF->PNG ({sz} bytes)")
        os.remove(out)
    except Exception as e:
        results.append(f"  FAIL: PDF->PNG -> {e}")
    
    # PDF -> DOCX
    out = os.path.join(base, "_diag_out.docx")
    try:
        # Suppress pdf2docx logging
        import logging
        logging.getLogger("pdf2docx").setLevel(logging.CRITICAL)
        FileConverter.pdf_to_docx(test_pdf, out)
        sz = os.path.getsize(out)
        results.append(f"  OK: PDF->DOCX ({sz} bytes)")
        os.remove(out)
    except Exception as e:
        results.append(f"  FAIL: PDF->DOCX -> {e}")

# DOCX -> PDF
if os.path.exists(test_docx):
    out = os.path.join(base, "_diag_out.pdf")
    try:
        FileConverter.docx_to_pdf(test_docx, out)
        sz = os.path.getsize(out)
        results.append(f"  OK: DOCX->PDF ({sz} bytes)")
        os.remove(out)
    except Exception as e:
        results.append(f"  FAIL: DOCX->PDF -> {e}")

# Image -> PDF (create a simple test image)
from PIL import Image
img_path = os.path.join(base, "_diag_test.jpg")
img = Image.new("RGB", (100, 100), "red")
img.save(img_path)
out = os.path.join(base, "_diag_out.pdf")
try:
    FileConverter.image_to_pdf(img_path, out)
    sz = os.path.getsize(out)
    results.append(f"  OK: IMG->PDF ({sz} bytes)")
    os.remove(out)
except Exception as e:
    results.append(f"  FAIL: IMG->PDF -> {e}")
os.remove(img_path)

results.append("\n=== DONE ===")

# Write to file
with open(os.path.join(base, "diag_results.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("\n".join(results))
