# American Presidency Archive Scraping
A Python project for scraping and analyzig documents from The [American Presidency Project](https://www.presidency.ucsb.edu/).

This source will be very useful for people who need linguistic data at some chosen temporal intervals (for example, years 2000 and 2024).

The toolset allows you to collect structured data from presidential speeches, debates, and other documents, save them in JSONL format, diagnose and validate the data, and perform basic text analysis.

The scraping is done with `requests` and `BeautifulSoup`.

## Features
* Web Scraping: Download speeches and documents by year from presidency.ucsb.edu.

* HTML Parsing: Extract structured metadata (title, date, person, role, etc.) and full text.

* Data Storage: Save results as JSONL files, one entry per line.

* Diagnostics: Check JSON/JSONL files for validity and structure issues.

* Text Analysis: Tokenize, count words, and analyze the most frequent terms (with optional stopword removal).

* Logging: Operations are logged for debugging and transparency.

## Usage
Edit the year range in `scraping/scrape_links.py` and run it.
```python
for year in range(2000, 2001):  # Change to desired range, e.g., range(1789, 2026)
    scrape_year(year, output_dir="output")
```
## Output Example
```jsonl
{
  "title": "Democratic Candidates Debate in Durham, New Hampshire",
  "date": "2000-01-05",
  "time": "19:00:00",
  "position": "",
  "context_role": "Primary and General Election Presidential Debates",
  "person_or_category": "Presidential Candidate Debates",
  "person_url": "https://www.presidency.ucsb.edu/people/other/presidential-candidate-debates",
  "presidential_number": "",
  "presidential_position": "",
  "term_dates": "",
  "source_url": "https://www.presidency.ucsb.edu/documents/democratic-candidates-debate-durham-new-hampshire-0",
  "text": "[full document text with newlines '\n']"
}
```
As you can see, the fields that can't be applied to a certain record are left blank.

## Customization
* Year Range: Change in the `scrape_links.py` script loop.

* Output Directory: Set via `scrape_year(year, output_dir=...)`.

* Analysis Options: Toggle stopword filtering in `analyze_file()`.

## Troubleshooting
* Scraping Too Fast: The script includes `time.sleep()` calls to avoid overloading the server. Adjust if needed.

* Parsing Errors: Check logs in `logs/` for details.

* NLTK Errors: Ensure `stopwords` and `punkt` are downloaded.

## Requirements
See 'requirements.txt' for all dependencies. Key packages used:

* requests

* beautifulsoup4

* nltk

* tqdm

* logging
