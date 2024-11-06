from datetime import date, datetime, timedelta
import unicodeit
import re
import json

def detexify(text):
    pattern = r' \[(.*?)\]'
    result = re.sub(pattern, '', text)

    pattern = r'[ \~\\]+cite{(.*?)\}'
    result = re.sub(pattern, '', result)

    return result

def detexify_data(data):
    for obj in data:
        obj['abstract'] = detexify(obj['abstract'])
    
    return data

def rekrijn_data(data):
    for obj in data:
        if 'Krijn Reijnders' in obj['authors']:
            obj['authors'] = ["Krĳn Reĳnders" if name == "Krijn Reijnders" else name for name in obj['authors']]

    return data

def untexcommand(data):
    return data

def clean_data(data):
    if isinstance(data, list):
        data = detexify_data(data)
        data = rekrijn_data(data)

    return data


with open('data.json', 'r') as f:
    data = json.load(f)
    papers = data["papers"]

last100 = clean_data(papers[:100])

with open('website_data.json', 'w') as f:
    json.dump(last100, f, indent=4)



