# Global variables shared across modules
import re
from urllib.parse import urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

BASE_URLS = {
    "metruyenchu": "https://metruyenchu.com.vn",
    "wikicv": "https://wikicv.net"
}

def extract_story_slug(url):
    """Extract story slug from URL"""
    m = re.search(r"https?://(?:wikicv\.net/truyen|metruyenchu\.com\.vn)/([^/]+)/", url)
    return m.group(1) if m else None

def get_base_url(url):
    """Get appropriate base URL based on domain"""
    if "metruyenchu" in url:
        return BASE_URLS["metruyenchu"]
    elif "wikicv.net" in url:
        return BASE_URLS["wikicv"]
    return None
