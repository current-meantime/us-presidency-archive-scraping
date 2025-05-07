import os
import math
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parse_html import parse_speech

def get_total_results(soup):
    header = soup.find("div", class_="view-header")
    if header:
        text = header.get_text()
        parts = text.strip().split()
        if "of" in parts:
            try:
                total = int(parts[parts.index("of") + 1])
                return total
            except:
                pass
    return 0

def get_speech_links(soup):
    base_url = "https://www.presidency.ucsb.edu"
    links = []
    for td in soup.select("td.views-field.views-field-title a"):
        href = td.get("href", "")
        if href.startswith("/documents/"):
            links.append(urljoin(base_url, href))
    return links  # usuń duplikaty

def save_jsonl(data, filepath):

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def scrape_year(year, output_dir):
    print(f"Rok {year}...")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{year}.jsonl")
    base_url = "https://www.presidency.ucsb.edu/advanced-search"
    params_base = {
        "from[date]": f"01-01-{year}",
        "to[date]": f"12-31-{year}",
        "items_per_page": 100,
        "page": 0
    }

    # pobierz pierwszą stronę i sprawdź liczbę wyników
    response = requests.get(base_url, params=params_base)
    soup = BeautifulSoup(response.text, "html.parser")
    total = get_total_results(soup)
    pages = math.ceil(total / 100)
    print(f"  - {total} wyników, {pages} stron")

    for page in range(14, 15):
        print(f"  - Strona {page + 1}/{pages}")
        params_base["page"] = page
        try:
            response = requests.get(base_url, params=params_base)
            soup = BeautifulSoup(response.text, "html.parser")
            links = get_speech_links(soup)
            print(f"    > {len(links)} linków")

            for link in links:
                try:
                    data = parse_speech(link)
                    save_jsonl(data, output_file)
                    time.sleep(0.5)  # by nie przeciążać serwera
                except Exception as e:
                    print(f"    [!] Błąd w przemowie: {link} — {e}")

        except Exception as e:
            print(f"  [!] Błąd strony {page}: {e}")
        time.sleep(1)

# uruchomienie dla wybranego zakresu lat
for year in range(2000, 2001): # max range: range(1789, 2026)
    scrape_year(year, output_dir="output")
