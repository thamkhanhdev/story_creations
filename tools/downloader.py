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
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
story_dir = os.path.join(parent_dir, "stories")
os.makedirs(story_dir, exist_ok=True)
os.makedirs(os.path.join(story_dir, "backup"), exist_ok=True)

result = None
for site_key, base_url in variables.BASE_URLS.items():
    if site_key in url:
        result = subprocess.run(["python", f"tools/web/{site_key}.py", url, story_name, story_dir])
        break
else:
    print("\033[93mUnsupported site\033[0m")
    sys.exit(1)