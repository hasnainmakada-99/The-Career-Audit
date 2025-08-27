import os
import pdfplumber
import docx
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# --- FIX: Explicitly set the path to the Tesseract executable ---
# This line is the correction. Make sure this path matches where you installed Tesseract.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# ----------------------------------------------------------------

def ocr_from_image(image):
    """Performs OCR on a single image object."""
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"--- TESSERACT ERROR ---")
        print(f"An error occurred during OCR: {e}")
        print("Please ensure Tesseract is installed and the path in parser.py is correct.")
        print("-----------------------")
        return ""

def parse_resume(file_path):
    """
    Parses a resume file (.pdf, .docx, .png, .jpg) and returns its text content.
    Includes OCR fallback for image-based PDFs.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at '{file_path}'"

    file_extension = os.path.splitext(file_path)[1].lower()
    full_text = ""

    try:
        # --- Handle PDF files (with OCR fallback) ---
        if file_extension == '.pdf':
            # 1. First, try standard text extraction
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
            
            # 2. If text is minimal, assume it's a scanned PDF and use OCR
            if len(full_text.strip()) < 100:
                print("Minimal text extracted. Attempting OCR fallback...")
                full_text = "" # Reset text to be filled by OCR
                images = convert_from_path(file_path)
                for img in images:
                    full_text += ocr_from_image(img) + "\n"

        # --- Handle DOCX files (no change here) ---
        elif file_extension == '.docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                full_text += para.text + "\n"

        # --- Handle Image files directly with OCR ---
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            image = Image.open(file_path)
            full_text = ocr_from_image(image)

        else:
            return "Error: Unsupported file type."

        cleaned_text = ' '.join(full_text.split())
        return cleaned_text

    except Exception as e:
        return f"Error processing file: {e}"