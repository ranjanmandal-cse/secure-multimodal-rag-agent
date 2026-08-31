import re
import fitz
import pytesseract
from PIL import Image


def normalize_ocr_text(text: str) -> str:
    """
    Normalize common OCR artifacts while preserving
    the original text as much as possible.
    """

    # OCR may misread the Indian rupee symbol in amounts.
    text = re.sub(
        r"(Amount\s*[:\-]?\s*)[%€]\s*(\d[\d,]*)",
        r"\1₹\2",
        text,
        flags=re.IGNORECASE,
    )

    # Handle OCR where the currency symbol is separated
    # from the amount.
    text = re.sub(
        r"(Amount\s*[:\-]?\s*)₹\s+(\d[\d,]*)",
        r"\1₹\2",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()


def extract_image_text(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return normalize_ocr_text(text)


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from a PDF.

    First attempts native PDF text extraction.
    If no usable text is found, renders PDF pages
    as images and applies Tesseract OCR.
    """

    document = fitz.open(pdf_path)

    extracted_pages = []

    for page in document:
        text = page.get_text()

        if text.strip():
            extracted_pages.append(text)
        else:
            # Scanned/image-only PDF page
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples,
            )

            ocr_text = pytesseract.image_to_string(image)

            if ocr_text.strip():
                extracted_pages.append(ocr_text)

    document.close()

    return normalize_ocr_text("\n".join(extracted_pages))

def extract_text(file_path: str, file_type: str = "") -> str:
    """
    Extract text from supported evidence files.
    """

    if file_type == "application/pdf" or file_path.lower().endswith(".pdf"):
        return extract_pdf_text(file_path)

    if file_type == "text/plain" or file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            text = file.read()

        return normalize_ocr_text(text)

    return extract_image_text(file_path)