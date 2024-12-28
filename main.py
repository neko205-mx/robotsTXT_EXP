import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse

def fetch_robots_txt(url):
    """Fetch robots.txt file from the given URL."""
    robots_url = urljoin(url, "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            print(f"[INFO] Successfully fetched robots.txt from {robots_url}")
            return response.text
        else:
            print(f"[ERROR] Failed to fetch robots.txt. HTTP Status: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] Error fetching robots.txt: {e}")
        return None

def extract_disallowed_paths(robots_txt):
    """Extract Disallow paths from robots.txt."""
    disallowed_paths = []
    for line in robots_txt.splitlines():
        line = line.strip()
        if line.startswith("Disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:  # Ignore empty disallows
                disallowed_paths.append(path)
    return disallowed_paths

def check_paths(url, paths):
    """Check the status code and title for each disallowed path."""
    for path in paths:
        full_url = urljoin(url, path)
        try:
            response = requests.get(full_url, timeout=10)
            status_code = response.status_code
            title = extract_title(response.text) if response.status_code == 200 else "N/A"
            print(f"[{status_code}] {full_url} - Title: {title}")
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {full_url}: {e}")

def extract_title(html_content):
    """Extract the title from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    title_tag = soup.find("title")
    return title_tag.text.strip() if title_tag else "No Title"

def main():
    parser = argparse.ArgumentParser(description="Fetch and analyze robots.txt for disallowed paths.")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://example.com)")
    args = parser.parse_args()

    url = args.url.strip()
    if not url.startswith("http"):
        url = "http://" + url

    robots_txt = fetch_robots_txt(url)
    if robots_txt:
        disallowed_paths = extract_disallowed_paths(robots_txt)
        print(f"[INFO] Found {len(disallowed_paths)} disallowed paths.")
        check_paths(url, disallowed_paths)

if __name__ == "__main__":
    main()
