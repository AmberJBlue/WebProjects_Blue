import requests
import datetime
from bs4 import BeautifulSoup
import json


# The only information given for this page is the name and price of the instrument
response = []

# Prepare for parsing with BeautifulSoup
url = 'https://play.google.com/store/apps/collection/topselling_free'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

# # Parse url
i = 1
for position in soup.find_all('div', class_='details'):
    name = position.find('a', class_='title').text
    desc = name
    name = name[4:].lstrip()
    # 'Find all digits(\d+) in string 'rank'
    rank = i
    desc = position.find('div', class_='description').text

    # Make changes to response
    i = i + 1
    response.append({'Rank': rank, 'Name': name, 'Description': desc})

# Write response to JSON file
today = str(datetime.datetime.now().date())
postingsFile = today + '.GoogleFree.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()
