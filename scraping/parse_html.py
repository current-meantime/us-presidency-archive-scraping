from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import logging
from logging_config import setup_logging

setup_logging()

example_url = "https://www.presidency.ucsb.edu/documents/democratic-candidates-debate-durham-new-hampshire-0"

def parse_speech(url):
    logging.info(f"Parsing speech from link: {url}")
    # the line below may be uncommented but the terminal can get cluttered as a result
    # print(f"Parsing speech from link: {url}")
    base_url = "https://www.presidency.ucsb.edu"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # treść przemówienia
    speech_div = soup.find("div", class_="field-docs-content")
    speech_text = speech_div.get_text(separator="\n", strip=True) if speech_div else ""

    # data i godzina
    date_span = soup.find("div", class_="field-docs-start-date-time")
    date_meta = date_span.find("span") if date_span else None
    date_content = date_meta["content"] if date_meta and "content" in date_meta.attrs else ""
    date_parts = date_content.split("T")
    date = date_parts[0] if date_parts else ""
    time = date_parts[1].split("+")[0] if len(date_parts) > 1 else ""

    # tytuł dokumentu
    title_div = soup.find("div", class_="field-ds-doc-title")
    doc_title = title_div.get_text(strip=True) if title_div else ""

    # osoba lub kategoria (w zależności od struktury)
    docs_person = soup.find("div", class_="field-docs-person")
    person_name = ""
    person_url = ""

    if docs_person:
        person_tag = docs_person.select_one("h3.diet-title a")
        if person_tag:
            person_name = person_tag.get_text(strip=True)
            person_url = urljoin(base_url, person_tag["href"])
        else:
            # fallback do kategorii (np. debates)
            fallback_title = docs_person.select_one(".field-title")
            person_name = fallback_title.get_text(strip=True) if fallback_title else ""

    # byline: numer, stanowisko, daty kadencji (jeśli dostępne)
    ordinal_number = ""
    position = ""
    term_dates = ""

    byline = docs_person.select_one("div.field-ds-byline")
    if byline:
        ordinal = byline.select_one(".presidential-ordinal-number")
        job = byline.select_one(".job-position")
        dates = byline.select_one(".dates")

        ordinal_number = ordinal.get_text(strip=True) if ordinal else ""
        position = job.get_text(strip=True) if job else ""
        term_dates = dates.get_text(strip=True) if dates else ""

    # dostosowanie zmiennych, aby rozdzielić rolę prezydenta i kontekst wydarzenia
    person_position = position if ordinal_number else ""  # dla prezydentów
    context_role = position if not ordinal_number else ""  # dla wydarzeń, jak debaty

    # jeśli brak prezydenta, upewnijmy się, że `presidential_position` nie zawiera danych o debacie
    presidential_position = person_position if ordinal_number else ""

    return {
        "title": doc_title,
        "date": date,
        "time": time,
        "position": person_position,  # jeśli prezydent, to jego pozycja
        "context_role": context_role,  # jeśli wydarzenie, to rola wydarzenia (np. Debata)
        "person_or_category": person_name,
        "person_url": person_url,
        "presidential_number": ordinal_number,
        "presidential_position": presidential_position,  # jeśli prezydent, jego stanowisko
        "term_dates": term_dates,
        "source_url": url,
        "text": speech_text
    }

# przykładowy URL
# speech_data = parse_speech("https://www.presidency.ucsb.edu/documents/democratic-candidates-debate-durham-new-hampshire-0")
# print(json.dumps(speech_data, ensure_ascii=False, indent=4))





