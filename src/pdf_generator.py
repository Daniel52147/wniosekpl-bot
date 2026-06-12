from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.documents import DocumentDef


DISCLAIMER_PL = (
    "Dokument wygenerowany przez WniosekPL (wersja bezpłatna). "
    "To pomocnik — nie jest dokumentem urzędowym. "
    "Przed złożeniem w urzędzie sprawdź aktualny formularz na stronie urzędu. "
    "Za poprawność danych odpowiada składający wniosek."
)


def generate_pdf(
    doc_def: DocumentDef,
    answers: dict[str, str],
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitlePL",
        parent=styles["Heading1"],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor("#1a365d"),
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.grey,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#744210"),
        backColor=colors.HexColor("#fffaf0"),
        borderPadding=6,
    )

    story: list = []
    story.append(Paragraph(doc_def.title_pl, title_style))
    story.append(
        Paragraph(
            f"Data wygenerowania: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            meta_style,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    rows = [["Pole (PL)", "Wartość"]]
    for field in doc_def.fields:
        value = answers.get(field.key, "").strip() or "—"
        rows.append([field.label_pl, value])

    table = Table(rows, colWidths=[7 * cm, 10 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7fafc")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.8 * cm))

    if doc_def.id == "umowa_najmu":
        story.extend(_umowa_clauses(answers, styles))

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(DISCLAIMER_PL, disclaimer_style))

    pdf = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    pdf.build(story)
    return output_path


def _umowa_clauses(answers: dict[str, str], styles) -> list:
    body = styles["Normal"]
    czynsz = answers.get("czynsz", "—")
    kaucja = answers.get("kaucja", "0")
    od = answers.get("data_od", "—")
    do = answers.get("data_do", "czas nieoznaczony")
    media = answers.get("media_opis", "—")
    lok = answers.get("adres_lokalu", "—")
    wyn = answers.get("wynajmujacy_imie_nazwisko", "—")
    naj = answers.get("najemca_imie_nazwisko", "—")

    text = f"""
    <b>§1 Przedmiot umowy</b><br/>
    Wynajmujący ({wyn}) oddaje Najemcy ({naj}) do używania lokal mieszkalny
    przy adresie: {lok}.<br/><br/>
    <b>§2 Czynsz i kaucja</b><br/>
    Czynsz miesięczny: {czynsz} PLN. Kaucja: {kaucja} PLN.<br/><br/>
    <b>§3 Okres najmu</b><br/>
    Od: {od}. Do: {do}.<br/><br/>
    <b>§4 Media</b><br/>
    {media}.<br/><br/>
    <b>§5 Postanowienia końcowe</b><br/>
    Umowa sporządzona w dwóch jednobrzmiących egzemplarzach. Strony oświadczają,
    że zapoznały się z treścią umowy.
    """
    return [Paragraph(text, body)]
