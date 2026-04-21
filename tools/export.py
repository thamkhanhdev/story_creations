import os
import sys
from fpdf import FPDF

def save_to_pdf(input_txt, output_pdf, title):
    pdf = FPDF()
    pdf.add_page()
    # Use font DejaVuSans (Supports Unicode well)
    font_path = os.path.join(os.path.dirname(__file__), "font", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path)
    pdf.set_font("DejaVu", size=12)

    with open(input_txt, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            pdf.multi_cell(0, 5, line)
            if i % 1000 == 0:
                print(f"\033[92m[LOG] Finished exporting {i} lines...\033[0m")

    pdf.output(output_pdf)
    print(f"\033[95m[LOG] Finished exporting to {output_pdf}\033[0m")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[93mPlease provide the story name, e.g.: python export.py \"Happy Ending\"\033[0m")
        sys.exit(1)

    story_name = sys.argv[1]
    input_txt = f"story/{story_name}/{story_name}.txt"
    output_pdf = f"story/{story_name}/{story_name}.pdf"

    print(f"\033[92m[LOG] Starting export of {story_name}.txt to {story_name}.pdf\033[0m")
    save_to_pdf(input_txt, output_pdf, story_name)
