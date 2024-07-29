import requests
from bs4 import BeautifulSoup

websitesToDisplay = []
linksOnPage = []


def connect(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def target():
    phrase = input('Enter the phrase you would like to find 5 wiki pages for: ')
    return phrase


def links(soup):
    global linksOnPage
    for link in soup.find_all('a'):
        linksOnPage.append(link.get('href'))
    return linksOnPage


def search(soup, target):
    page = soup.get_text().lower()
    target_lower = target.lower()
    if target_lower in page:
        found = True
    else:
        found = False
    return found


def searchLinks(soup, target):
    global linksOnPage
    global websitesToDisplay
    linksOnPage = links(soup)
    while len(websitesToDisplay) < 5:
        i = 0
        while i < len(linksOnPage):
            link = linksOnPage[i]
            if link and link[:6] == "/wiki/":
                fullLink = "https://en.wikipedia.org" + link
                linkConnect = connect(fullLink)
                found = search(linkConnect, target)
                if found:
                    websitesToDisplay.append(fullLink)
                newLinks = links(linkConnect)
                for item in newLinks:
                    linksOnPage.append(item)
            i += 1


def output(targetPhrase):
    global websitesToDisplay
    print("5 Wikipedia pages including the phrase", targetPhrase, "are: ")
    for page in websitesToDisplay[:5]:
        print(page)


targetPhrase = target()
soupReturn = connect("https://en.wikipedia.org/wiki/Main_Page")
searchLinks(soupReturn, targetPhrase)
output(targetPhrase)