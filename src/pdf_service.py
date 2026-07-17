import logging
from pathlib import Path

from src.documents import DocumentDef
from src.official_forms import generate_official_pdf, has_official_template
from src.pdf_generator import generate_pdf as generate_helper_pdf

logger = logging.getLogger(__name__)


def generate_document_pdf(
    doc_def: DocumentDef,
    answers: dict[str, str],
    output_path: Path,
) -> tuple[Path, str]:
    """
    Returns (path, mode) where mode is 'official' or 'helper'.
    """
    if has_official_template(doc_def.id):
        try:
            path = generate_official_pdf(doc_def.id, answers, output_path)
            return path, "official"
        except Exception:
            logger.warning(
                "Official PDF generation failed for %s; falling back to helper PDF",
                doc_def.id,
                exc_info=True,
            )
            path = generate_helper_pdf(doc_def, answers, output_path)
            return path, "helper_fallback"

    path = generate_helper_pdf(doc_def, answers, output_path)
    return path, "helper"
