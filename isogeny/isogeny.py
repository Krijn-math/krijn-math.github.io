import os
import requests
import unicodeit
import re
import mdtex2html
from bs4 import BeautifulSoup

def detexify(text):
    def repl(match):
        return str(unicodeit.replace((match.group(1))))

    pattern = r'\$(.*?)\$'
    result = re.sub(pattern, repl, text)
    return result

url = "https://eprint.iacr.org/search?q=isogeny+isogenies"

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")

search_results = soup.find_all("div", class_="mb-4")
total = len(search_results)

file_name = f"papers.txt"

with open(file_name, "w") as file:
    for index, result in enumerate(search_results, start=1):
        title = result.find("strong").get_text().strip()
        authors = result.find("span", class_="fst-italic").get_text().strip()
        id = result.find("a", class_="paperlink").get_text().strip()

        title = detexify(title)

        file.write(f"{title.lower()};;;")
        file.write(f"{authors.lower()};;;")
        file.write(f"{id}\n")


print("Scraping and saving complete!")
