"""Render Gopi_Kancharla_Resume.txt to an ATS-safe PDF.

Single column, selectable text, standard fonts, no tables/graphics/headers or
footers - the layout Workday and similar parsers handle most reliably.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageTemplate,
    Paragraph,
    Spacer,
)

import sys

HERE = Path(__file__).resolve().parent
# Usage: build_resume_pdf.py [source.txt] [output.pdf] [pdf-title]
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "Gopi_Kancharla_Resume.txt"
OUTPUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "pdfs" / "Gopi_Kancharla_Resume.pdf"
PDF_TITLE = sys.argv[3] if len(sys.argv) > 3 else "Gopi K Kancharla - Resume"

NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#147D82")
INK = colors.HexColor("#202B36")
MUTED = colors.HexColor("#526271")
LIGHT = colors.HexColor("#C9D6DE")

SECTIONS = {
    "PROFESSIONAL SUMMARY",
    "CORE COMPETENCIES",
    "PROFESSIONAL EXPERIENCE",
    "ENTREPRENEURIAL AND 0-TO-1 PLATFORM LEADERSHIP",
    "PATENTS, PUBLICATIONS, AND THOUGHT LEADERSHIP",
    "EDUCATION",
    "CERTIFICATIONS",
    "LOCATION AND WORK AUTHORIZATION",
    "LOCATION AND AVAILABILITY",
}

COMPANIES = (
    "TOYOTA FINANCIAL SERVICES",
    "CAPITAL ONE",
    "DELL EMC / EMC CORPORATION",
    "IPC SYSTEMS INC.",
    "ADESA INC.",
    "IBM -",
)

styles = {
    "name": ParagraphStyle(
        "name", fontName="Helvetica-Bold", fontSize=21, leading=25,
        textColor=NAVY, spaceAfter=3,
    ),
    "contact": ParagraphStyle(
        "contact", fontName="Helvetica", fontSize=8.6, leading=12.4,
        textColor=MUTED,
    ),
    "target": ParagraphStyle(
        "target", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
        textColor=TEAL, spaceBefore=9, spaceAfter=1,
    ),
    "targetsub": ParagraphStyle(
        "targetsub", fontName="Helvetica", fontSize=8.6, leading=11.6,
        textColor=MUTED,
    ),
    "section": ParagraphStyle(
        "section", fontName="Helvetica-Bold", fontSize=10.2, leading=13,
        textColor=NAVY, spaceBefore=10, spaceAfter=2.5,
    ),
    "company": ParagraphStyle(
        "company", fontName="Helvetica-Bold", fontSize=9.8, leading=12.6,
        textColor=INK, spaceBefore=7, spaceAfter=0,
    ),
    "role": ParagraphStyle(
        "role", fontName="Helvetica-Bold", fontSize=8.9, leading=11.6,
        textColor=TEAL, spaceAfter=0,
    ),
    "body": ParagraphStyle(
        "body", fontName="Helvetica", fontSize=8.9, leading=12.2,
        textColor=INK, spaceAfter=4,
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=8.9, leading=11.9,
        textColor=INK, leftIndent=11, bulletIndent=1, spaceAfter=2.2,
    ),
}


def build():
    lines = SOURCE.read_text(encoding="utf-8").split("\n")
    flow = []

    # Header block: name, contact lines, then the target-title line.
    flow.append(Paragraph(escape(lines[0]), styles["name"]))
    for raw in lines[1:4]:
        flow.append(Paragraph(escape(raw), styles["contact"]))
    flow.append(Paragraph(escape(lines[5]), styles["target"]))
    flow.append(Paragraph(escape(lines[6]), styles["targetsub"]))
    flow.append(Spacer(1, 3))
    flow.append(HRFlowable(width="100%", thickness=0.8, color=LIGHT,
                           spaceBefore=5, spaceAfter=1))

    for raw in lines[7:]:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        if stripped in SECTIONS:
            flow.append(Paragraph(escape(stripped), styles["section"]))
            flow.append(HRFlowable(width="100%", thickness=0.6, color=LIGHT,
                                   spaceBefore=0, spaceAfter=5))
            continue

        if stripped.startswith(COMPANIES):
            flow.append(Paragraph(escape(stripped), styles["company"]))
            continue

        if stripped.startswith("- "):
            flow.append(Paragraph(escape(stripped[2:]), styles["bullet"],
                                  bulletText="-"))
            continue

        # Role/date lines carry a date range or a pipe-delimited skill row.
        if any(t in stripped for t in ("/20", "- Present")) and len(stripped) < 130:
            flow.append(Paragraph(escape(stripped), styles["role"]))
            continue

        flow.append(Paragraph(escape(stripped), styles["body"]))

    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=LETTER,
        leftMargin=0.62 * inch, rightMargin=0.62 * inch,
        topMargin=0.52 * inch, bottomMargin=0.5 * inch,
        title=PDF_TITLE,
        author="Gopi K Kancharla",
        subject="Resume",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame])])
    doc.build(flow)
    print(f"Wrote: {OUTPUT}")


if __name__ == "__main__":
    build()
