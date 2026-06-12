from pathlib import Path

import fitz


def add_preview_watermark(source: Path, dest: Path) -> Path:
    """Duplikat PDF z diagonalnym znakiem PODGLAD."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(source))
    label = "PODGLAD WniosekPL — NIE SKLADAC W URZEDZIE"
    for page in doc:
        rect = page.rect
        page.insert_text(
            (rect.width * 0.25, rect.height * 0.55),
            label,
            fontsize=18,
            fontname="helv",
            color=(0.75, 0.1, 0.1),
            rotate=45,
        )
    doc.save(str(dest), garbage=4, deflate=True)
    doc.close()
    return dest
