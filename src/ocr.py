"""Extract text from uploaded PDF/image documents."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def ocr_engine_status() -> dict:
    tesseract = bool(shutil.which("tesseract"))
    try:
        import pytesseract  # noqa: F401

        pytesseract_ok = True
    except Exception:
        pytesseract_ok = False
    try:
        from PIL import Image  # noqa: F401

        pillow_ok = True
    except Exception:
        pillow_ok = False
    return {
        "tesseract_binary": tesseract,
        "pytesseract": pytesseract_ok,
        "pillow": pillow_ok,
        "ready": tesseract and pytesseract_ok and pillow_ok,
    }


def extract_text(path: Path) -> str:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}:
        return _extract_image(path)
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:20000]
    except OSError:
        return ""


def _extract_pdf(path: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except Exception:
        return ""
    chunks: list[str] = []
    with fitz.open(path) as doc:
        for page in doc:
            chunks.append(page.get_text("text") or "")
            if sum(len(c) for c in chunks) > 20000:
                break
    text = "\n".join(chunks).strip()
    if text:
        return text[:20000]
    # Scanned PDF: render first pages and OCR if possible.
    status = ocr_engine_status()
    if not status["ready"]:
        return (
            "[PDF looks image-only — install Tesseract for OCR, "
            "or paste key phrases into the AI chat]"
        )
    ocr_bits: list[str] = []
    try:
        import fitz
        import pytesseract
        from PIL import Image
        import io

        with fitz.open(path) as doc:
            for i, page in enumerate(doc):
                if i >= 3:
                    break
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_bits.append(pytesseract.image_to_string(img, lang="pol+eng") or "")
    except Exception:
        logger.warning("PDF OCR failed", exc_info=True)
        return ""
    return "\n".join(ocr_bits).strip()[:20000]


def _extract_image(path: Path) -> str:
    status = ocr_engine_status()
    if status["ready"]:
        try:
            import pytesseract
            from PIL import Image

            img = Image.open(path)
            text = pytesseract.image_to_string(img, lang="pol+eng") or ""
            if text.strip():
                return text.strip()[:20000]
        except Exception:
            logger.warning("Image OCR failed", exc_info=True)
    return (
        "[image uploaded — OCR engine not ready; "
        "install tesseract-ocr + pytesseract, or describe the letter in chat]"
    )
