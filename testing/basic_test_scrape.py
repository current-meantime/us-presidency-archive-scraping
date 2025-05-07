from bs4 import BeautifulSoup
import requests

url = "https://www.presidency.ucsb.edu/documents/joint-statement-strategic-stability-cooperation-initiative-between-the-united-states"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
transcript = soup.find("div", class_="field-docs-content").text
print(transcript)