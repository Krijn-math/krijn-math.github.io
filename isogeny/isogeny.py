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

# Define the URL to scrape
url = "https://eprint.iacr.org/search?q=isogeny+isogenies"

# Send a GET request to the URL and retrieve the HTML content
response = requests.get(url)
html_content = response.text

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find all the search result elements on the page
search_results = soup.find_all("div", class_="mb-4")
total = len(search_results)

# Create a directory to store the text files
# directory = "/home/krijn/Documents/Mathematics/Website/krijn-math.github.io/isogeny"
# os.makedirs(directory, exist_ok=True)



file_name = f"papers2.txt"
# file_path = os.path.join(website_directory, file_name)

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
