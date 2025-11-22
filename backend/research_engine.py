import requests
from bs4 import BeautifulSoup
import html2text
from backend.conflict_detector import detect_conflicts


# Convert HTML to plain text
def clean_html(html):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    return converter.handle(html)

# Get web page content
def fetch_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers, timeout=3)
        res.raise_for_status()
        return clean_html(res.text)
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

# Get search results (Bing scraper)
def bing_search(query, count=3):
    urls = []
    search_url = f"https://www.bing.com/search?q={query}"
    res = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.select("li.b_algo h2 a")

    for r in results[:count]:
        urls.append(r["href"])

    return urls

# Full research pipeline
def research_company(company_name):
    query = f"{company_name} company overview"
    urls = bing_search(query, count=3)

    research_data = {}

    # 1. Scrape all results
    for url in urls:
        print("Scraping URL:", url)
        try:
            text = fetch_page(url)
            research_data[url] = text
        except Exception as e:
            research_data[url] = f"Error fetching page: {e}"

    # 2. Detect conflicts across all scraped sources
    conflicts = detect_conflicts(research_data)

    # 3. Return both data and detected conflicts
    return {
        "data": research_data,
        "conflicts": conflicts
    }
