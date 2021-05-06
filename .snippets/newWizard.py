# TO DO:
# Clean the link list from irrelevant websites (line 27)
'''
socnetworks = [
"https://www.facebook.com",
"https://www.vk.com",
"https://twitter.com"
]
'''

import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.request import urlretrieve

# Making a search query and making a list of resulted links
def getLinks(query):
    searcher = 'https://epicsearch.in/search?pno=1&q='
    url = searcher + query.replace(' ', '%20')
    res = requests.get(url)

    # Return if epicsearch server is not responding
    if not res.ok:
        print('Search server is not responding')
        return

    soup = BeautifulSoup(res.text, 'lxml')
    links = soup.findAll('a',{'class':'Title'})

    # Return if there are zero search results
    if links == []:
        print('Nothing was found')
        return

    urls = [link['href'] for link in links]
    return urls

# Extracting and organizing the text and the top image from a site
def Scrape(site):
    # Get the article's text and top image
    article = Article(site)
    article.download()
    article.parse()
    text = article.text
    top_image = article.top_image
    # Separate the text into paragraphs by new lines
    paragraphs = [p for p in text.splitlines() if p!='']

    # Identify the headers by finding their length
    def isHeader(string):
        words = string.split(' ')
        if len(words) <= 10:
            return True
        else:
            return False

    # Create paragraph:header pairs dictionary (use None with no header)
    slides = {}
    firstIter = True
    for p in paragraphs:
        # Skip if the paragraph is a header
        if isHeader(p):
            firstIter = False
            continue
        # Check if the previous paragraph is a header
        if not firstIter:
            previous = paragraphs[paragraphs.index(p)-1]
            if isHeader(previous):
                slides[p] = previous
            else:
                slides[p] = None
        # Add with None if it's the first paragraph and not a header
        else:
            slides[p] = None
            firstIter = False
    # Return the slide structures and the top image
    return slides, top_image

if __name__ == '__main__':
    # Replace it with the form input from flask later
    topic = input('Topic: ')
    sites = getLinks(topic)
    print('Getting',sites[0],'\n')
    slides, top_image = Scrape(sites[0])

    ###
    for slide in slides:
        print(slides[slide],'\n',slide,'\n'*3)
    print(top_image)
