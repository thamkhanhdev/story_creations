import requests, time
from bs4 import BeautifulSoup
import sys
import subprocess
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Add parent directory (tools/) to sys.path to import variables
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import variables

if len(sys.argv) < 4:
    print("\033[93mUsage: python metruyenhot.py <start_url> <story_name> <story_dir>\033[0m")
    sys.exit(1)

start_url = sys.argv[1]
story_name = sys.argv[2]
story_dir = sys.argv[3]
base_url = variables.BASE_URLS["metruyenhot"]

# Register Vietnamese font (adjust path if needed)
try:
    font_path = os.path.join(os.path.dirname(__file__), "../font/DejaVuSans.ttf")
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("DejaVu", font_path))
        font_name = "DejaVu"
    else:
        font_name = "Arial"

    font_path_bold = os.path.join(os.path.dirname(__file__), "../font/DejaVuSans-Bold.ttf")
    if os.path.exists(font_path_bold):
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", font_path_bold))
        font_name_bold = "DejaVu-Bold"
    else:
        font_name_bold = "Arial-Bold"
except:
    font_name = "Arial"
    font_name_bold = "Arial-Bold"

# Create PDF doc
pdf_file = f"{story_dir}\\{story_name}.pdf"
txt_file = f"{story_dir}\\backup\\{story_name}.txt"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*cm, bottomMargin=0.5*cm)
story = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor="#000000",
    spaceAfter=12,
    fontName=f"{font_name_bold}",
    alignment=1  # Center alignment
)
content_style = ParagraphStyle(
    'CustomContent',
    parent=styles['Normal'],
    fontSize=11,
    leading=18,
    alignment=4,  # Justify
    fontName=font_name,
    spaceAfter=6
)

# Also write TXT file
with open(txt_file, "w", encoding="utf-8") as txt_f:
    url = start_url
    chapter_num = 1

    while url:
        print(f"[LOG] Loading chapter {chapter_num}: {url}")
        for attempt in range(3):
            r = requests.get(url, headers=variables.headers)
            if r.status_code == 200:
                break
            time.sleep(0.5)
        if r.status_code != 200:
            print(f"\033[91m[LOG] Server error at {url}, skipping.\033[0m")
            break

        soup = BeautifulSoup(r.text, "html.parser")

        # Extract title
        title_div = soup.find("div", class_="rv-chapt-title")
        title_tag = title_div.find("h2") if title_div else soup.find("h2")
        title = title_tag.get_text(strip=True) if title_tag else f"Chapter {chapter_num}"

        # Extract content
        content_div = soup.find("div", class_="chapter-c")
        if content_div:
            text = content_div.get_text("\n", strip=True)
        else:
            text = ""

        # Write to TXT
        txt_f.write(f"\n\n--- {title} ---\n\n")
        for line in text.splitlines():
            line = line.strip()
            if line:
                txt_f.write(line + "\n")

        # Add to PDF
        if chapter_num > 1:
            story.append(PageBreak())  # New page for each chapter
        story.append(Paragraph(title, title_style))
        story.append(Spacer(0.5, 0.3*cm))

        # Split content into paragraphs
        for para_text in text.split("\n"):
            para_text = para_text.strip()
            if para_text:
                story.append(Paragraph(para_text.replace("\n", "<br/>"), content_style))

        # Next chapter
        next_button = soup.find("a", string="Tiếp")
        url = next_button["href"] if next_button else None
        if url and not url.startswith("http"):
            url = base_url + url
        chapter_num += 1

print(f"Finished saving story to {txt_file}")

# Build PDF
try:
    doc.build(story)
    print(f"\033[35m[LOG] PDF created: {pdf_file}\033[0m")
except Exception as e:
    print(f"\033[91m[ERROR] Failed to create PDF: {e}\033[0m")
