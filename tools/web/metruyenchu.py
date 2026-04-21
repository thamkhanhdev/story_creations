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
    print("\033[93mUsage: python metruyenchu.py <start_url> <story_name> <file_name>\033[0m")
    sys.exit(1)

start_url = sys.argv[1]
story_name = sys.argv[2]
file_name = sys.argv[3]
base_url = variables.BASE_URLS["metruyenchu"]

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
pdf_file = file_name.replace(".txt", ".pdf")
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
with open(file_name, "w", encoding="utf-8") as txt_f:
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
        title = soup.find("h1").get_text(strip=True)
        content_div = soup.find("div", class_="truyen")
        text = content_div.get_text("\n", strip=True) if content_div else ""

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

        next_button = soup.select_one("a.next")
        if next_button and next_button.get("href") and next_button["href"] != "#":
            next_url = next_button["href"]
            if next_url.startswith("/"):
                url = base_url + next_url
            else:
                url = next_url
            chapter_num += 1
            time.sleep(0.05)
        else:
            print("OK")
            break

print(f"\033[92mFinished saving story to {file_name}\033[0m")

# Build PDF
try:
    doc.build(story)
    print(f"\033[35m[LOG] PDF created: {pdf_file}\033[0m")
except Exception as e:
    print(f"\033[91m[ERROR] Failed to create PDF: {e}\033[0m")
