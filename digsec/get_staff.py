from datetime import date, datetime, timedelta
import requests
from bs4 import BeautifulSoup

url = "https://cs.ru.nl/staff/index.html"

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")

search_results = soup.find_all("a")
staff = []

for thing in search_results:
    thing = str(thing)
    start = thing.find("(")
    
    if start == -1:
        continue

    start += + 1
    mid = thing.find(")") 
    end = thing.find("</a>")
    
    firstname = thing[start:mid]
    surname = thing[mid+2:end]
    
    staff.append(firstname + " " + surname)


file_name = f"staff.txt"
with open(file_name, "w") as file:
        for name in staff:
            file.write(name + ",")

    
