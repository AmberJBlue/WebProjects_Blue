import requests
import datetime
from bs4 import BeautifulSoup
import json

# The only information given for this page is the name and price of the instrument
response = []

# Prepare for parsing with BeautifulSoup
url = 'https://play.google.com/store/apps/collection/topselling_paid?hl=en'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

# # Parse url
i = 1
for position in soup.find_all('div', class_='details'):
    name = position.find('a', class_='title').text
    name = name[4:].lstrip()
    rank = i
    # rank = ''.join(rank)
    desc = position.find('div', class_='description').text
    price = position.find('span', class_='display-price').text
    i = i + 1

    # Make changes to response
    response.append({'Rank': rank, 'Name': name, 'Description': desc, 'Price': price})
#
# # Write response to JSON file
today = str(datetime.datetime.now().date())
postingsFile = today + '.GooglePaid.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()
