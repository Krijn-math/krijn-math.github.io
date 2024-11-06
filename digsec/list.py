from datetime import date, datetime, timedelta
from random import shuffle
import unicodeit
import re
import json

with open('staff.txt', 'r') as f:
    staff = f.read().split(',')

def detexify(text):
    pattern = r' \[(.*?)\]'
    result = re.sub(pattern, '', text)

    pattern = r'[ \~\\]+cite{(.*?)\}'
    result = re.sub(pattern, '', result)

    result = re.sub(r'\${2}(.*?)\${2}', r'\\[ \1 \\]', result)
    result = re.sub(r'\$(.*?)\$', r'\\( \1 \\)', result)

    return result

def detexify_data(data):
    for obj in data:
        obj['abstract'] = detexify(obj['abstract'])
        obj['title'] = re.sub(r'\$(.*?)\$', r'\\( \1 \\)', obj['title'])
    
    return data

def rekrijn_data(data):
    for obj in data:
        if 'Krijn Reijnders' in obj['authors']:
            obj['authors'] = ["Krĳn Reĳnders" if name == "Krijn Reijnders" else name for name in obj['authors']]

    return data

def radboudify(data):
    for obj in data:
        obj['radboud'] = 'false'

        for author in obj['authors']:
            if author in staff:
                obj['radboud'] = 'true'

    return data

def clean_data(data):
    if isinstance(data, list):
        data = detexify_data(data)
        data = radboudify(data)
        data = rekrijn_data(data)

    return data


with open('short_data.json', 'r') as f:
    papers = json.load(f)
    # data = json.load(f)
    # papers = data["papers"]

papers = radboudify(papers)

lastweek = []
timer = True
i = 0
while len(lastweek) < 100:
    parsed_date = datetime.strptime(papers[i]['lastmodified'], '%Y-%m-%d %H:%M:%S')
    current_date = datetime.now()
    time_diff = current_date - parsed_date

    if time_diff <= timedelta(days=7) or papers[i]['radboud'] == "true":
        lastweek.append(papers[i])
    
    i += 1
    
    # if time_diff > timedelta(days = 100):
    #     timer = False

lastweek = clean_data(lastweek)

shuffle(lastweek)

with open('website_data.json', 'w') as f:
    json.dump(lastweek, f, indent=4)



