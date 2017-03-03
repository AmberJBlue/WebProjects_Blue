import requests
import datetime

today = str(datetime.datetime.now().date())

# Scraping the listings of synthesizers on Sweetwater, Reverb, and Chicago Music Exchange
sites = {
    'Apple Store - Free' : 'http://www.apple.com/itunes/charts/free-apps/',
    'Apple Store - Paid' : 'http://www.apple.com/itunes/charts/paid-apps/',
    'Google Play - Free' : 'https://play.google.com/store/apps/collection/topselling_free',
    'Google Play - Paid' : 'https://play.google.com/store/apps/collection/topselling_paid?hl=en'
         }

for name, link in sites.items():
    response = requests.get(link)
    html = response.content

    fileName = today + '.' + name + '.html'
    outfile = open(fileName, "wb")
    outfile.write(html)
    outfile.close()