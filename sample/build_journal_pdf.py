#!/usr/bin/env python3
"""
The People's Register — Field Journal PDF Pipeline (portfolio sample)
=====================================================================

A self-contained, runnable sample of the production pipeline used to
generate the downloadable PDF edition of the field journal.

    $ python3 build_journal_pdf.py --issue "Vol. 01" --output journal.pdf

The full production pipeline extends this core with:
  * per-issue content models (editorial, six cluster chapters, metrics)
  * versioned release outputs (?v=2) and secure asset embedding
  * Brevo newsletter issue-alert triggers on release

This sample is intentionally dependency-light (reportlab only) so it can
be read, run, and judged on its own.

Author: Rowan Sampson — Digital Origin
"""

import argparse
from datetime import date

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

# ---------------------------------------------------------------- brand tokens
INK = HexColor("#1a2430")
GREEN = HexColor("#2f7d54")
GOLD = HexColor("#b8860b")
SLATE = HexColor("#5a6472")
LINE = HexColor("#d9dfe7")


# ---------------------------------------------------------------- content model
ISSUES = {
    "Vol. 01": {
        "title": "The People Have Answered",
        "subtitle": "Six Clusters. One Movement.",
        "clusters": [
            ("Molly Blackburn", "Wards 1-9, 12, 39, 40",
             "Metro central and the NMU & TVET campus drives, where youth mobilisation went viral."),
            ("Lilian Diedericks", "Wards 10, 11, 13, 29, 31, 32, 34, 35, 37, 38",
             "Door to door across the high-density Northern Areas, Gelvandale to Booysens Park."),
            ("Govan Mbeki", "Wards 14-22, 24",
             "New Brighton and KwaZakhele: the historic heartland's highest registration results."),
            ("Champion Galela", "Wards 24-28, 30, 33, 36, 41",
             "Kariega and Despatch: from a comrade's funeral to the registration table."),
            ("Alex Matikinca", "Wards 23, 53-60",
             "Motherwell, Ikamvalihle and Coega: the growth corridor and its information tables."),
            ("Zola Nqini", "Wards 42-52",
             "KwaNobuhle's outer ring: the industrial working class answering the call."),
        ],
    }
}


# ---------------------------------------------------------------- typography
def style(name, **kw):
    return ParagraphStyle(name, **kw)

S_NAME = style("name", fontName="Helvetica-Bold", fontSize=22, leading=26,
               textColor=INK, alignment=TA_CENTER)
S_KICK = style("kick", fontName="Helvetica", fontSize=9, leading=12,
               textColor=GOLD, alignment=TA_CENTER, spaceAfter=2)
S_H    = style("h", fontName="Helvetica-Bold", fontSize=11, leading=14,
               textColor=INK, spaceBefore=10, spaceAfter=4)
S_BODY = style("body", fontName="Helvetica", fontSize=9.5, leading=13,
               textColor=INK, spaceAfter=5)


def build_journal(issue_key, out_path):
    issue = ISSUES[issue_key]

    doc = BaseDocTemplate(
        out_path, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=20 * mm, bottomMargin=18 * mm,
        title=f"The People's Register — {issue_key}",
        author="The People's Register",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])

    story = []

    # ------------------------------------------------------------ masthead
    story.append(Paragraph("THE PEOPLE'S REGISTER", S_NAME))
    story.append(Paragraph(f"FIELD JOURNAL · {issue_key} · {date.today():%d %B %Y}", S_KICK))
    story.append(HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceBefore=4, spaceAfter=6))

    story.append(Paragraph(issue["title"], S_H))
    story.append(Paragraph(issue["subtitle"], S_BODY))

    # ------------------------------------------------------------ clusters
    rows = [[Paragraph(f"<b>{name}</b>", S_BODY),
             Paragraph(wards, S_BODY),
             Paragraph(focus, S_BODY)]
            for name, wards, focus in issue["clusters"]]
    t = Table(rows, colWidths=[38 * mm, 42 * mm, 90 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    doc.build(story)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a field journal PDF.")
    parser.add_argument("--issue", default="Vol. 01", choices=list(ISSUES))
    parser.add_argument("--output", default="peoples-register.pdf")
    args = parser.parse_args()

    path = build_journal(args.issue, args.output)
    print(f"built: {path}")
