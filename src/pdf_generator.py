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

    if doc_def.id == "pismo_do_urzedu":
        story.extend(_letter_body(answers, styles))
    elif doc_def.id == "upowaznienie":
        story.extend(_upowaznienie_body(answers, styles))
    elif doc_def.id == "oswiadczenie_dochodow":
        story.extend(_oswiadczenie_body(answers, styles))
    else:
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


def _letter_body(answers: dict[str, str], styles) -> list:
    body = styles["Normal"]
    right = ParagraphStyle("RightMeta", parent=body, alignment=2)
    nadawca = answers.get("nadawca_imie_nazwisko", "—")
    adres = answers.get("nadawca_adres", "—")
    kontakt = answers.get("nadawca_telefon", "—")
    urzad = answers.get("urzad_nazwa", "—")
    urzad_adres = answers.get("urzad_adres", "—")
    znak = answers.get("znak_sprawy", "brak") or "brak"
    temat = answers.get("temat_pisma", "—")
    tresc = answers.get("tresc_pisma", "—").replace("\n", "<br/>")
    data = answers.get("data_pisma", "—")
    miasto = answers.get("miejscowosc_pisma", "—")

    return [
        Paragraph(f"{miasto}, dnia {data}<br/>{nadawca}<br/>{adres}<br/>{kontakt}", right),
        Spacer(1, 0.6 * cm),
        Paragraph(f"<b>{urzad}</b><br/>{urzad_adres}", body),
        Spacer(1, 0.5 * cm),
        Paragraph(f"<b>Znak sprawy:</b> {znak}", body),
        Paragraph(f"<b>Dotyczy:</b> {temat}", body),
        Spacer(1, 0.4 * cm),
        Paragraph("Szanowni Państwo,", body),
        Spacer(1, 0.25 * cm),
        Paragraph(tresc, body),
        Spacer(1, 0.5 * cm),
        Paragraph("Z poważaniem,", body),
        Spacer(1, 1.2 * cm),
        Paragraph(f"…………………………………<br/>{nadawca}", body),
    ]


def _upowaznienie_body(answers: dict[str, str], styles) -> list:
    body = styles["Normal"]
    text = f"""
    Ja, niżej podpisany/a <b>{answers.get('mocodawca_imie_nazwisko', '—')}</b>,
    dokument: {answers.get('mocodawca_dokument', '—')},
    zamieszkały/a: {answers.get('mocodawca_adres', '—')},<br/><br/>
    upoważniam <b>{answers.get('pelnomocnik_imie_nazwisko', '—')}</b>,
    dokument: {answers.get('pelnomocnik_dokument', '—')},<br/><br/>
    do: {answers.get('zakres_upowaznienia', '—')}<br/><br/>
    w: {answers.get('urzad_nazwa', '—')}.<br/><br/>
    {answers.get('miejscowosc_upowaznienia', '—')}, dnia {answers.get('data_upowaznienia', '—')}.
    <br/><br/>
    …………………………………<br/>
    podpis mocodawcy
    """
    return [Paragraph(text, body)]


def _oswiadczenie_body(answers: dict[str, str], styles) -> list:
    body = styles["Normal"]
    text = f"""
    Ja, niżej podpisany/a <b>{answers.get('imie', '—')} {answers.get('nazwisko', '—')}</b>,
    urodzony/a {answers.get('data_urodzenia', '—')},
    zamieszkały/a: {answers.get('adres_zamieszkania', '—')},<br/><br/>
    oświadczam, że moje źródło dochodu to: <b>{answers.get('zrodlo_dochodu', '—')}</b>.<br/>
    Pracodawca / płatnik: {answers.get('pracodawca_nazwa', '—') or '—'}.<br/>
    Dochód miesięczny netto: <b>{answers.get('dochod_miesieczny', '—')} PLN</b>.<br/>
    Okres: {answers.get('okres_dochodu', '—')}.<br/><br/>
    Jestem świadomy/a odpowiedzialności karnej za złożenie fałszywego oświadczenia.<br/><br/>
    {answers.get('miejscowosc_oswiadczenia', '—')}, dnia {answers.get('data_oswiadczenia', '—')}.
    <br/><br/>
    …………………………………<br/>
    podpis
    """
    return [Paragraph(text, body)]


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
