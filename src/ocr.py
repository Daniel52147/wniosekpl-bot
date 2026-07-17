"""Extract text from uploaded PDF/image documents."""

from __future__ import annotations

from pathlib import Path


def extract_text(path: Path) -> str:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}:
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
            chunks.append(page.get_text("text"))
            if sum(len(c) for c in chunks) > 20000:
                break
    return "\n".join(chunks).strip()[:20000]


def _extract_image(path: Path) -> str:
    # Best-effort OCR via PyMuPDF pixmap OCR is unavailable without Tesseract.
    # We still accept images and return a placeholder for LLM/manual explanation.
    try:
        import fitz
    except Exception:
        return ""
    try:
        with fitz.open(path) as doc:
            if doc.page_count:
                return (
                    "[image uploaded — OCR engine not installed; "
                    "describe the letter in chat or install tesseract for full OCR]"
                )
    except Exception:
        return ""
    return ""
