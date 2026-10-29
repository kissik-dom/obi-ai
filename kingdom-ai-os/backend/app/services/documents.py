"""Bounded PDF/document rendering primitives for Kingdom AI OS.

This module formats provided content; it does not invent missing book chapters.
"""
from __future__ import annotations

import io
import re
from html import escape
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, LETTER, legal
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether, HRFlowable
)

PAGE_SIZES = {"A4": A4, "LETTER": LETTER, "LEGAL": legal}
FONTS = {"Helvetica", "Times-Roman", "Courier"}
GOLD = colors.HexColor("#B08D35")
NAVY = colors.HexColor("#14233B")


def _clean_text(value: Any, max_len: int = 200_000) -> str:
    if not isinstance(value, str):
        return str(value)[:max_len]
    return value[:max_len]


def _paragraph_text(value: str) -> str:
    # ReportLab Paragraph supports a small XML-like markup; escape all source text.
    return escape(value).replace("\n", "<br/>")


class StyledBookDoc(BaseDocTemplate):
    def __init__(self, output, *, pagesize, title, author, quote, margins):
        self.book_title = title
        self.book_author = author
        self.footer_quote = quote
        left, right, top, bottom = margins
        super().__init__(output, pagesize=pagesize, title=title, author=author,
                         leftMargin=left, rightMargin=right, topMargin=top, bottomMargin=bottom)
        frame = Frame(left, bottom, pagesize[0] - left - right, pagesize[1] - top - bottom,
                      id="normal", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="book", frames=[frame], onPage=self._decorate))

    def _decorate(self, canvas, doc):
        canvas.saveState()
        w, h = self.pagesize
        # Every page receives the requested signature footer, including the title page.
        if doc.page >= 1:
            y = 0.48 * inch
            canvas.setStrokeColor(GOLD)
            canvas.setLineWidth(1.15)
            canvas.line(doc.leftMargin, y + 0.14 * inch, w - doc.rightMargin, y + 0.14 * inch)
            cx = w / 2
            diamond = 4
            path = canvas.beginPath()
            path.moveTo(cx, y + 0.14 * inch + diamond)
            path.lineTo(cx + diamond, y + 0.14 * inch)
            path.lineTo(cx, y + 0.14 * inch - diamond)
            path.lineTo(cx - diamond, y + 0.14 * inch)
            path.close()
            canvas.setFillColor(GOLD)
            canvas.drawPath(path, stroke=0, fill=1)
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(NAVY)
            if self.footer_quote:
                q = self.footer_quote[:180]
                canvas.drawCentredString(w / 2, y + 0.29 * inch, q)
            canvas.drawRightString(w - doc.rightMargin, 0.25 * inch, str(doc.page))
        canvas.restoreState()


def render_pdf(payload: dict[str, Any]) -> bytes:
    title = _clean_text(payload.get("title", "Untitled Document"), 300).strip() or "Untitled Document"
    subtitle = _clean_text(payload.get("subtitle", ""), 500)
    author = _clean_text(payload.get("author", ""), 200)
    quote = _clean_text(payload.get("footer_quote", ""), 180).replace("\n", " ")
    font = payload.get("font", "Times-Roman")
    if font not in FONTS:
        font = "Times-Roman"
    page_size_name = payload.get("page_size", "A4")
    pagesize = PAGE_SIZES.get(page_size_name, A4)
    margin_in = payload.get("margin_inches", 0.85)
    try:
        margin_in = float(margin_in)
    except (TypeError, ValueError):
        margin_in = 0.85
    margin_in = min(max(margin_in, 0.45), 1.5)
    margins = (margin_in * inch,) * 4

    sections = payload.get("sections", [])
    if not isinstance(sections, list) or len(sections) > 250:
        raise ValueError("sections must be a list with no more than 250 entries")
    total_chars = 0
    for section in sections:
        if not isinstance(section, dict):
            raise ValueError("each section must be an object")
        total_chars += len(str(section.get("body", ""))) + len(str(section.get("title", "")))
    if total_chars > 3_000_000:
        raise ValueError("document content exceeds the 3 million character render limit")

    output = io.BytesIO()
    doc = StyledBookDoc(output, pagesize=pagesize, title=title, author=author, quote=quote, margins=margins)
    base = getSampleStyleSheet()
    cover_title = ParagraphStyle("CoverTitle", parent=base["Title"], fontName=font, fontSize=28, leading=34,
                                 alignment=TA_CENTER, textColor=NAVY, spaceAfter=22)
    cover_sub = ParagraphStyle("CoverSub", parent=base["Normal"], fontName=font, fontSize=15, leading=21,
                               alignment=TA_CENTER, textColor=GOLD, spaceAfter=16)
    h1 = ParagraphStyle("SectionHeading", parent=base["Heading1"], fontName=font, fontSize=18,
                        leading=23, textColor=NAVY, spaceBefore=12, spaceAfter=12, keepWithNext=True)
    body_style = ParagraphStyle("BookBody", parent=base["BodyText"], fontName=font, fontSize=11,
                                leading=16, alignment=TA_JUSTIFY, spaceAfter=9, allowWidows=0, allowOrphans=0)
    small = ParagraphStyle("Small", parent=base["BodyText"], fontName=font, fontSize=9, leading=12, spaceAfter=5)

    story = [Spacer(1, 1.7 * inch), Paragraph(_paragraph_text(title), cover_title)]
    if subtitle:
        story.append(Paragraph(_paragraph_text(subtitle), cover_sub))
    story.append(Spacer(1, 0.45 * inch))
    story.append(HRFlowable(width="48%", thickness=1.4, color=GOLD, hAlign="CENTER"))
    if author:
        story.extend([Spacer(1, 0.3 * inch), Paragraph(_paragraph_text(author), ParagraphStyle(
            "Author", parent=base["Normal"], fontName=font, fontSize=12, alignment=TA_CENTER, textColor=NAVY))])
    story.append(PageBreak())

    toc = payload.get("include_contents", True)
    if toc and sections:
        story.append(Paragraph("Contents", h1))
        for index, section in enumerate(sections, start=1):
            label = _clean_text(section.get("title", f"Section {index}"), 300)
            story.append(Paragraph(f"{index}. {_paragraph_text(label)}", small))
        if payload.get("include_glossary", True):
            story.append(Paragraph(f"{len(sections)+1}. Glossary", small))
        if payload.get("references"):
            story.append(Paragraph(f"{len(sections)+2 if payload.get('include_glossary', True) else len(sections)+1}. References", small))
        story.append(PageBreak())

    for index, section in enumerate(sections, start=1):
        section_title = _clean_text(section.get("title", f"Section {index}"), 300).strip()
        body = _clean_text(section.get("body", ""), 1_500_000)
        story.append(Paragraph(_paragraph_text(section_title or f"Section {index}"), h1))
        # Paragraphs are kept as paragraphs, preserving line breaks and chunk boundaries.
        for para in re.split(r"\n\s*\n", body.strip()):
            para = para.strip()
            if para:
                story.append(Paragraph(_paragraph_text(para), body_style))
        story.append(Spacer(1, 0.12 * inch))

    glossary = payload.get("glossary", [])
    if payload.get("include_glossary", True):
        story.append(PageBreak())
        story.append(Paragraph("Glossary", h1))
        glossary_count = 0
        if isinstance(glossary, list):
            for item in glossary[:1000]:
                if isinstance(item, dict) and item.get("term"):
                    term = _clean_text(item["term"], 200)
                    definition = _clean_text(item.get("definition", ""), 1500)
                    story.append(Paragraph(f"<b>{_paragraph_text(term)}</b> — {_paragraph_text(definition)}", body_style))
                    glossary_count += 1
        if not glossary_count:
            story.append(Paragraph("Glossary terms have not yet been supplied. Generate and verify the glossary before publication.", body_style))
    references = payload.get("references", [])
    if isinstance(references, list) and references:
        story.append(PageBreak())
        story.append(Paragraph("References", h1))
        for index, reference in enumerate(references[:3000], 1):
            story.append(Paragraph(f"{index}. {_paragraph_text(_clean_text(reference, 2000))}", body_style))
    doc.build(story)
    return output.getvalue()


def render_docx(payload: dict[str, Any]) -> bytes:
    """Create an editable DOCX using the same book structure and footer motif."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.section import WD_SECTION
    from docx.shared import Inches, Pt, RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    title = _clean_text(payload.get("title", "Untitled Document"), 300).strip() or "Untitled Document"
    subtitle = _clean_text(payload.get("subtitle", ""), 500)
    author = _clean_text(payload.get("author", ""), 200)
    font_name = _clean_text(payload.get("font", "Times-Roman"), 100)
    font_name = {"Times-Roman": "Times New Roman", "Helvetica": "Arial", "Courier": "Courier New"}.get(font_name, font_name)
    quote = _clean_text(payload.get("footer_quote", ""), 180)
    sections = payload.get("sections", [])
    if not isinstance(sections, list) or len(sections) > 250:
        raise ValueError("sections must be a list with no more than 250 entries")
    if sum(len(str(x.get("body", ""))) for x in sections if isinstance(x, dict)) > 3_000_000:
        raise ValueError("document content exceeds the 3 million character render limit")

    doc = Document()
    sec = doc.sections[0]
    margin = min(max(float(payload.get("margin_inches") or 0.85), 0.45), 1.5)
    sec.top_margin = Inches(margin); sec.bottom_margin = Inches(margin)
    sec.left_margin = Inches(margin); sec.right_margin = Inches(margin)
    normal = doc.styles['Normal']; normal.font.name = font_name; normal.font.size = Pt(11)
    for style_name in ('Title', 'Heading 1', 'Heading 2'):
        doc.styles[style_name].font.name = font_name
        doc.styles[style_name].font.color.rgb = RGBColor(20, 35, 59)
    doc.core_properties.title = title
    doc.core_properties.author = author

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Inches(1.7)
    r = p.add_run(title); r.bold = True; r.font.name = font_name; r.font.size = Pt(28); r.font.color.rgb = RGBColor(20, 35, 59)
    if subtitle:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(subtitle); r.font.name = font_name; r.font.size = Pt(15); r.font.color.rgb = RGBColor(176, 141, 53)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('━━━━━━━━━━━━━━━━ ◆ ━━━━━━━━━━━━━━━━'); r.font.color.rgb = RGBColor(176, 141, 53); r.font.name = font_name
    if author:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(author); r.font.name = font_name; r.font.size = Pt(12)
    doc.add_page_break()

    if payload.get("include_contents", True):
        doc.add_heading('Contents', level=1)
        for index, item in enumerate(sections, 1):
            doc.add_paragraph(f"{index}. {_clean_text(item.get('title', f'Section {index}'), 300)}")
        if payload.get("include_glossary", True):
            doc.add_paragraph(f"{len(sections)+1}. Glossary")
        if payload.get("references"):
            doc.add_paragraph(f"{len(sections)+2 if payload.get('include_glossary', True) else len(sections)+1}. References")
        doc.add_page_break()
    for index, item in enumerate(sections, 1):
        doc.add_heading(_clean_text(item.get('title', f'Section {index}'), 300), level=1)
        for paragraph in re.split(r"\n\s*\n", _clean_text(item.get('body', ''), 1_500_000).strip()):
            if paragraph.strip():
                p = doc.add_paragraph(paragraph.strip())
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    glossary = payload.get('glossary', [])
    if payload.get('include_glossary', True):
        doc.add_page_break(); doc.add_heading('Glossary', level=1)
        glossary_count = 0
        if isinstance(glossary, list):
            for item in glossary[:1000]:
                if isinstance(item, dict) and item.get('term'):
                    p = doc.add_paragraph()
                    r = p.add_run(_clean_text(item['term'], 200) + ' — '); r.bold = True
                    p.add_run(_clean_text(item.get('definition', ''), 1500)); glossary_count += 1
        if not glossary_count:
            doc.add_paragraph('Glossary terms have not yet been supplied. Generate and verify the glossary before publication.')
    references = payload.get('references', [])
    if isinstance(references, list) and references:
        doc.add_page_break(); doc.add_heading('References', level=1)
        for index, reference in enumerate(references[:3000], 1):
            doc.add_paragraph(f"{index}. {_clean_text(reference, 2000)}")

    footer = sec.footer
    fp = footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if quote:
        qr = fp.add_run(quote); qr.font.name = font_name; qr.font.size = Pt(8); qr.font.color.rgb = RGBColor(20, 35, 59)
    table = footer.add_table(rows=1, cols=3, width=Inches(6.2))
    table.autofit = False
    widths = [Inches(2.05), Inches(2.05), Inches(2.1)]
    for cell, width in zip(table.rows[0].cells, widths):
        cell.width = width
        tc_pr = cell._tc.get_or_add_tcPr()
        borders = tc_pr.first_child_found_in('w:tcBorders')
        if borders is None:
            borders = OxmlElement('w:tcBorders'); tc_pr.append(borders)
        bottom = OxmlElement('w:bottom'); bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '8'); bottom.set(qn('w:color'), 'B08D35'); borders.append(bottom)
    table.cell(0,1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    diamond = table.cell(0,1).paragraphs[0].add_run('◆'); diamond.font.color.rgb = RGBColor(176, 141, 53)
    page_p = table.cell(0,2).paragraphs[0]; page_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    page_p.add_run('Page ')
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE'); page_p._p.append(fld)

    output = io.BytesIO(); doc.save(output); return output.getvalue()
