from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, HRFlowable, PageBreak, PageTemplate, Paragraph, Spacer


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Gopi_Kancharla_VP_Engineering_Resume.txt"
OUTPUT = ROOT / "output" / "pdf" / "Gopi_Kancharla_VP_Engineering_Resume.pdf"

NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#147D82")
INK = colors.HexColor("#202B36")
MUTED = colors.HexColor("#526271")
LIGHT = colors.HexColor("#D8E3E8")

SECTIONS = {
    "EXECUTIVE PROFILE",
    "VP ENGINEERING LEADERSHIP HIGHLIGHTS",
    "CORE LEADERSHIP AND TECHNICAL EXPERTISE",
    "PROFESSIONAL EXPERIENCE",
    "AI-NATIVE ENGINEERING AND PLATFORM TRANSFORMATION",
    "ENTREPRENEURIAL LEADERSHIP - FOUNDER AND 0-TO-1 PLATFORM BUILDING",
    "PATENTS, PUBLICATIONS, AND LEADERSHIP",
    "EDUCATION AND CERTIFICATIONS",
    "LOCATION",
}

COMPANIES = (
    "TOYOTA FINANCIAL SERVICES",
    "CAPITAL ONE",
    "DELL EMC / EMC CORPORATION",
    "IPC SYSTEMS INC.",
    "ADESA INC.",
    "IBM -",
)


def styles():
    base = getSampleStyleSheet()["Normal"]
    return {
        "name": ParagraphStyle("name", parent=base, fontName="Helvetica-Bold", fontSize=19, leading=21, textColor=NAVY, alignment=1, spaceAfter=2),
        "tag": ParagraphStyle("tag", parent=base, fontName="Helvetica-Bold", fontSize=9.2, leading=11, textColor=TEAL, alignment=1, spaceAfter=3),
        "contact": ParagraphStyle("contact", parent=base, fontSize=7.8, leading=9.5, textColor=MUTED, alignment=1),
        "section": ParagraphStyle("section", parent=base, fontName="Helvetica-Bold", fontSize=9.6, leading=11, textColor=NAVY, spaceBefore=6, spaceAfter=3, keepWithNext=True),
        "company": ParagraphStyle("company", parent=base, fontName="Helvetica-Bold", fontSize=8.8, leading=10.5, textColor=NAVY, spaceBefore=5, spaceAfter=1, keepWithNext=True),
        "role": ParagraphStyle("role", parent=base, fontName="Helvetica-BoldOblique", fontSize=8.25, leading=10, textColor=TEAL, spaceAfter=1.5, keepWithNext=True),
        "body": ParagraphStyle("body", parent=base, fontSize=8.2, leading=10.5, textColor=INK, spaceAfter=3),
        "bullet": ParagraphStyle("bullet", parent=base, fontSize=8.0, leading=10.2, textColor=INK, leftIndent=10, firstLineIndent=-6, bulletIndent=2, spaceAfter=1.5),
        "skills": ParagraphStyle("skills", parent=base, fontSize=7.8, leading=10, textColor=INK, spaceAfter=1.2),
    }


class ResumeDocument(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=LETTER, leftMargin=0.58 * inch, rightMargin=0.58 * inch, topMargin=0.48 * inch, bottomMargin=0.48 * inch, title="Gopi K Kancharla - VP Engineering Resume", author="Gopi K Kancharla")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="resume", frames=[frame], onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setFont("Helvetica-Bold", 7.5)
            canvas.setFillColor(NAVY)
            canvas.drawString(doc.leftMargin, LETTER[1] - 0.23 * inch, "GOPI K KANCHARLA | VP ENGINEERING")
            canvas.setStrokeColor(LIGHT)
            canvas.line(doc.leftMargin, LETTER[1] - 0.31 * inch, LETTER[0] - doc.rightMargin, LETTER[1] - 0.31 * inch)
        canvas.setStrokeColor(LIGHT)
        canvas.line(doc.leftMargin, 0.32 * inch, LETTER[0] - doc.rightMargin, 0.32 * inch)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 0.20 * inch, "haigopi@gmail.com | +1 469 388 2798 | Frisco, Texas")
        canvas.drawRightString(LETTER[0] - doc.rightMargin, 0.20 * inch, f"Page {doc.page}")
        canvas.restoreState()


def story(lines):
    style = styles()
    result = [
        Paragraph(escape(lines[0]), style["name"]),
        Paragraph(escape(lines[1]), style["tag"]),
        Paragraph(escape(lines[2]), style["contact"]),
        Paragraph(escape(lines[3]), style["contact"]),
        Paragraph(escape(lines[4]), style["contact"]),
        Spacer(1, 3),
        HRFlowable(width="100%", thickness=1.2, color=TEAL, spaceAfter=4),
    ]
    section = ""
    for line in lines[5:]:
        line = line.strip()
        if not line:
            continue
        if line in SECTIONS:
            section = line
            if line == "PROFESSIONAL EXPERIENCE":
                result.append(PageBreak())
            result.append(Paragraph(escape(line), style["section"]))
            result.append(HRFlowable(width="100%", thickness=0.55, color=LIGHT, spaceAfter=2))
        elif line.startswith(COMPANIES):
            result.append(Paragraph(escape(line), style["company"]))
        elif line.startswith("-"):
            result.append(Paragraph(escape(line[1:].strip()), style["bullet"], bulletText="•"))
        elif line.startswith(("Head of Technology", "Director, Software Engineering", "Senior Cloud Software", "Frontend Engineering", "Lead Software Engineer", "Technical Lead")):
            result.append(Paragraph(escape(line), style["role"]))
        elif section == "CORE LEADERSHIP AND TECHNICAL EXPERTISE":
            result.append(Paragraph(escape(line), style["skills"]))
        else:
            result.append(Paragraph(escape(line), style["body"]))
    return result


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    ResumeDocument(str(OUTPUT)).build(story(lines))
    print(OUTPUT)


if __name__ == "__main__":
    main()
