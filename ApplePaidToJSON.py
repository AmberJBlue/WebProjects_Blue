import requests
import datetime
from bs4 import BeautifulSoup
import json

# The only information given for this page is the name and price of the instrument
response = []
allDesc = []

# Prepare for parsing with BeautifulSoup
url = 'http://www.apple.com/itunes/charts/paid-apps/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

# # Parse url
for position in soup.find_all('li'):  # 17 'none'
    if position.find('strong') != None:
        rank = position.find('strong').string.replace(".", "")
        name = position.find('h3').string
        cat = position.find('h4').string
        link = position.find('a').get('href')
        # Going to the app page
        itemUrl = link
        itemPage = requests.get(itemUrl)
        itemSoup = BeautifulSoup(itemPage.content, 'lxml')
        #
        try:
            for center in itemSoup.find_all('div', class_="center-stack"):
                desc = center.find('p').text
            for left in itemSoup.find_all('div', id="left-stack"):
                # This try/except statement is to catch the AttributeError generated when a 'NoneType' is given
                # giving the output 'Information Not Available' - added after the if/else statements which accomplish the same thing
                try:
                    # Release date of the application
                    release = left.find('span', itemprop='datePublished').string
                    # Version (number) of the application
                    version = left.find('span', itemprop="softwareVersion").string
                    # IOS compatibility
                    compatibility = left.find('span', itemprop="operatingSystem").string.replace('Requires ', '')
                    # The current rating of the app
                    if left.find('div', class_="rating") is not None:
                        currentRating = left.find('div', class_="rating").get('aria-label')
                        # convert 'str' currentRating to string
                        str(currentRating)
                        if currentRating.find('and a half') == 2:
                            currentRating = currentRating[0] + '.5'
                        else:
                            currentRating = currentRating[0]
                    # The second (identical) 'Overall Ratings" class
                    if left.find('div', class_="rating") is not None:
                        if left.find('div', class_="rating").next_sibling is not None:
                            if left.find('div', class_="rating").next_sibling.next_sibling is not None:
                                if left.find('div',
                                             class_="rating").next_sibling.next_sibling.next_sibling.next_sibling is not None:
                                    ovRating = left.find('div',
                                                         class_="rating").next_sibling.next_sibling.next_sibling.next_sibling.get(
                                        'aria-label')
                                if ovRating.find('and a half') == 2:
                                    ovRating = ovRating[0] + '.5'
                                    # numOfRatings
                                else:
                                    ovRating = ovRating[0]
                            else:
                                ovRating = 'Information Not Available'

                    if left.find('span', class_="rating-count") is not None:
                        numOfCurrentRatings = left.find('span', class_="rating-count").string.replace(' Ratings', '')
                    allRatings = left.find('div', class_="rating")
                    # Some over excessive checking
                    if allRatings.next_sibling.next_sibling is not None:
                        if allRatings.next_sibling.next_sibling.next_sibling is not None:
                            if allRatings.next_sibling.next_sibling.next_sibling.next_sibling is not None:
                                numOfAllRatings = allRatings.next_sibling.next_sibling.next_sibling.next_sibling.find(
                                    'span',
                                    class_='rating-count')
                                numOfAllRatings = numOfAllRatings.string.replace(' Ratings', '')
                    else:
                        numOfAllRatings = 'Information Not Available'

                        # a variable saving a point in the elements | the location of the 'size' element
                    spot = left.find('li', class_="release-date").next_sibling.next_sibling
                    size = spot.text.replace('Size:', '')
                    ageLimit = left.find('div', class_="app-rating").next_element.string.replace('for the following:', '')
                    if spot.next_sibling.next_sibling.find('span', itemprop="name") is not None:
                        seller = spot.next_sibling.next_sibling.find('span', itemprop="name").string
                    else:
                        seller = 'Information Not Available'

                    if left.find('div', class_="extra-list in-app-purchases"):
                        inAppPurchasesBool = True

                        if inAppPurchasesBool == True:
                            inAppPurchases = 'Yes'
                        else:
                            inAppPurchases = 'No'
                    else:
                        inAppPurchases = 'Information Not Available'

                    price = left.find('div', itemprop="price").string
                except AttributeError:
                    print('Information Not Available')
        except AttributeError:
            print('Information Not Available')

            # Make changes to response
            allDesc.append({'The': desc})
            response.append(
                {'Rank': rank, 'Name': name, 'Category': cat, 'Description': desc, 'Release': release, 'Version': version,
                 'Compatibility': compatibility, 'Size': size, 'Age Restriction': ageLimit, 'Seller': seller,
                 'Rating of Current Version': currentRating,
                 'Number of Reviews (Current Versions) ': numOfCurrentRatings, 'Overall Rating': ovRating,
                 'Number of Reviews (All Time)': numOfAllRatings,
                 'In App Purchases': inAppPurchases, 'Price': price})


            # price = position.find('em', class_='product__price').text.strip()



# Write response to JSON file
today = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time())
postingsFile = today + time + '.ApplePaid.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()


# descFile = today + time + '.ApplePaidDescriptions.txt'
#
# with open(descFile, 'w') as outfile:
#     json.dump(allDesc, outfile, sort_keys=True, indent=2)
#
# outfile.close()

