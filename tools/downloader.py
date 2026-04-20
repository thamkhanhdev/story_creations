import sys
import subprocess
import os
import variables

if len(sys.argv) < 2:
    print("Usage: python downloader.py <url>")
    sys.exit(1)

url = sys.argv[1]
# Extract story name from URL using variables module
story_name = variables.extract_story_slug(url)
if not story_name:
    story_name = "story"
os.makedirs(f"story/{story_name}", exist_ok=True)
file_name = f"story/{story_name}/{story_name}.txt"

result = None
if "metruyenchu" in url:
    result = subprocess.run(["python", "tools/web/metruyenchu.py", url, story_name, file_name])
elif "wikicv.net" in url:
    result = subprocess.run(["python", "tools/web/wikicv.py", url, story_name, file_name])
else:
    print("\033[93mUnsupported site\033[0m")

if result is not None and result.returncode == 0:
    subprocess.run(["python", "tools/export.py", story_name])
elif result is not None:
    print(f"\033[91m[ERROR] Download process failed with return code {result.returncode}. Skipping export.\033[0m")