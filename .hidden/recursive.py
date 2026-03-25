import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://192.168.1.16/.hidden/"
IGNORE_SIZE = 34

def crawl(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[error] {url} -> {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href in ("../", "./") or href.startswith("?") or href.startswith("#"):
            continue

        if href.endswith("/"):
            result = crawl(urljoin(url, href))
            if result:
                return result
        elif href == "README":
            file_url = urljoin(url, href)
            try:
                resp = requests.get(file_url, timeout=10)
                resp.raise_for_status()
                size = len(resp.content)
                print(f"Readme found with {size} octets")
                if size != IGNORE_SIZE:
                    return file_url, resp.text.strip()
            except requests.RequestException:
                pass

if __name__ == "__main__":
    result = crawl(BASE_URL)
    if result:
        url, content = result
        print(f"\nTrouve : {url}")
    else:
        print("\nAucun README interessant.")
