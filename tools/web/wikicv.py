import requests, time
from bs4 import BeautifulSoup
import sys
import subprocess
import os

# Add parent directory (tools/) to sys.path to import variables
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import variables

if len(sys.argv) < 4:
    print("\033[93mUsage: python wikicv.py <start_url> <story_name> <file_name>\033[0m")
    sys.exit(1)

start_url = sys.argv[1]
story_name = sys.argv[2]
file_name = sys.argv[3]
base_url = variables.BASE_URLS["wikicv"]

with open(file_name, "w", encoding="utf-8") as f:
    url = start_url
    chapter_num = 1

    while url:
        print(f"[LOG] Loading chapter {chapter_num}: {url}")
        for attempt in range(3):
            r = requests.get(url, headers=variables.headers)
            if r.status_code == 200:
                break
            time.sleep(0.05)
        if r.status_code != 200:
            print(f"\033[91m[LOG] Server error at {url}, skipping.\033[0m")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        content_root = soup.find("div", id="bookContent")
        title_parts = [p.get_text(strip=True) for p in content_root.find_all("p", class_="book-title")] if content_root else []
        title = " - ".join(title_parts) if title_parts else ""
        content_body = soup.find("div", id="bookContentBody")
        paragraphs = content_body.find_all("p") if content_body else []
        text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        f.write(f"\n\n--- {title} ---\n\n")
        for line in text.splitlines():
            line = line.strip()
            if line:
                f.write(line + "\n")

        next_button = None
        for a in soup.find_all("a", class_="btn-bot"):
            if "Chương sau" in a.get_text():
                next_button = a
                break

        if next_button and next_button.get("href") and next_button["href"] != "#":
            next_url = next_button["href"]
            if next_url.startswith("/"):
                url = base_url + next_url
            else:
                url = next_url
            chapter_num += 1
            time.sleep(0.01)
        else:
            print("OK")
            break

print(f"\033[95mFinished saving story to {file_name}\033[0m")
