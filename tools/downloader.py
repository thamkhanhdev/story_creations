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
for site_key, base_url in variables.BASE_URLS.items():
    if site_key in url:
        result = subprocess.run(["python", f"tools/web/{site_key}.py", url, story_name, file_name])
        break
else:
    print("\033[93mUnsupported site\033[0m")
    sys.exit(1)