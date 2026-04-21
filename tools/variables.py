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
    "wikicv": "https://wikicv.net",
    "metruyenhot": "https://metruyenhot.me"
}

_DOMAIN_TO_BASE = {base.replace("https://", ""): base for base in BASE_URLS.values()}

def extract_story_slug(url):
    """Extract story slug from URL"""
    # Build pattern from BASE_URLS for maintainability
    domains = "|".join(BASE_URLS.values()).replace("https://", "").replace(".", r"\.")
    pattern = rf"https?://(?:{domains})/(?:truyen/)?([^/]+)/"
    m = re.search(pattern, url)
    return m.group(1) if m else None

def get_base_url(url):
    """Get appropriate base URL based on domain"""
    domain = urlparse(url).netloc
    return _DOMAIN_TO_BASE.get(domain)
