from datetime import date, datetime, timedelta
import json
import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
import os

base = "https://eprint.iacr.org/"
api = "api/1.0/"
end = "?auth=i@cr_indexing"
key = '/Annots'
uri = '/URI'
ank = '/A'
year = 2024

try:
    with open(f'eprint/eprintdata{year}.json', 'r') as f:
        papers = json.load(f)
    id = int(papers[-1]['pid'])
except:
    papers = []
    id = 0

def append_to_json(file_path, json_object):
    # Check if file exists and if it's empty
    file_exists = os.path.exists(file_path)
    if file_exists and os.path.getsize(file_path) > 0:
        # Open the file in read+write mode
        with open(file_path, "r+") as file:
            file.seek(0, os.SEEK_END)  # Go to the end of the file
            file.seek(file.tell() - 1, os.SEEK_SET)  # Move back one character to overwrite the closing ]
            
            # Insert a comma if there are already objects in the array
            file.write(",\n" if file.tell() > 1 else "\n")
            json.dump(json_object, file, indent=4)
            file.write("\n]")  # Close the JSON array
    else:
        # Create a new JSON array if the file is empty or does not exist
        with open(file_path, "w") as file:
            json.dump([json_object], file, indent=4)  # Start with a new array

def get_json(year,id):
    id = str(id)
    while len(id) < 3:
        id = '0' + id

    response = requests.get(base + api + str(year) + "/" + id + end)  
    assert response.status_code == 200
    
    response = response.json()
    exists = (response != {'error': 'No such paper'})

    return exists, response

def get_pdf(json):
    urlid = json['pdffile']
    pdfres = requests.get(base + urlid)
    pdf_io_bytes = io.BytesIO(pdfres.content)
    pdf = PyPDF2.PdfReader(pdf_io_bytes)

    return pdf

def extract_all_urls(pdf):
    urls = []

    pages = len(pdf.pages)

    for page in range(pages):
        page_slice = pdf.pages[page]
        page_obj = page_slice.get_object()
        if key in page_obj.keys():
            ann = page_obj[key]
            for a in ann:
                u = a.get_object()
                if uri in u[ank].keys():
                    urls.append(u[ank][uri])

    return urls

def extract_gits(urls):
    if urls == []:
        print("no urls given")
        return []
    
    gits = []
    gits += [ r for r in urls if 'git' in r]

    return gits

def get_repo(pdf):
    urls = extract_all_urls(pdf)

    if urls == []:
        print("no urls")
        return ['none']
    
    gits = extract_gits(urls)

    if gits == []:
        print("no git")
        return ['none']

    return gits


good_resp = True

while good_resp:
    id += 1
    print(id)
    good_resp, paper = get_json(year, id)
    repo = ['none']
    try:
        repo = get_repo(get_pdf(paper))
    except:
        print('failed to read repo')
    paper['repo'] = repo
    # papers.append(paper)
    append_to_json(f'eprint/eprintdata{year}.json', paper)

print(f'done up to eprint {year}/{id - 1}')

# for paper in papers:
#     try:
#         pdf = get_pdf(paper)
#         paper['gits'] = get_repo(pdf)
#     except:
#         print(f"error on {paper['name']}")
#         continue

#     if paper['gits'] != []:
#         print(f"{paper['name']} has repo {paper['gits'][0]}")
    
# with open('git_data.json', 'w') as f:
#     json.dump(papers, f, indent=4)
