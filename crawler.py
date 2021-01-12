# Built-in python libraries
import os                                               # for creating directories for the images
import re                                               # for content identification
import urllib.request                                   # for downloading the images

# Third party libraries
import requests                                         # for loading webpages
import urllib3                                          # for catching more errors
from urllib import request                              # for a faster image downloading
from bs4 import BeautifulSoup                           # for navigarting webpages
import bleach                                           # for cleaning NavigableStrings from tags
from selenium import webdriver                          # for seeing dynamic javascript pages // firefox browser and geckodriver in path required
from selenium.common.exceptions import TimeoutException # for handling the specific TimeoutException

# Built-in pptWizard libraries
from txtProcessor import *

# Search() will make a query search in the epic search engine and return a website's soup
def Search(query):
    print("Creating a search query...")
    # Collect the search results page
    search = "https://epicsearch.in/search?pno=1&q={0}".format(query)
    results = BeautifulSoup(requests.get(search).text,'lxml')

    # Identify the websites that are not suitable for the content extraction
    socnetworks = [
    "https://www.facebook.com",
    "https://www.vk.com",
    "https://twitter.com"
    ]

    # Find an available website
    for link in results.find_all('a', class_='Title'):
        print("\nReading through the website\n{0}".format(link.get("href")))

        # Skip the not suitable websites
        flag = 0
        for http in socnetworks:
            if re.search(http,link.get("href")):
                print("\nThis page is a social network page.")
                flag = 1
        if flag:
            continue

        try:
            # See if the website is giving a response
            response = requests.get(link.get("href"))
            if not response.ok:
                print("\nNo response " + str(response.status_code))
                continue
            site = BeautifulSoup(response.text,'lxml')
            # Final step after the site passed all the checks
            try:
                # Try to structurize the websites content
                structure = Memorize(site)
                if structure[2] == []:
                    print("\nThis website has no paragraphs.")
                    continue
                return structure
            # In case the website has an inapropriate structure
            except ValueError:
                print("\nThis website is not suitable.")
                continue
        # Skip the link if the site timed out
        except (TimeoutError, requests.exceptions.ConnectionError):
            print("\nIt took too long for the page to load.")
            continue
    # Return None if no accessible website can be found
    print("\nNothing was Found.")
    return None

# Memorize() will return a structure, which is a list,
# where its elements, building blocks for the presentation, are stored as following:
# structure[0] = Main_Title
# structure[1] = List_of_all_headlines
# structure[2] = List_of_all_paragraphs
def Memorize(soup):
    print("\nCollecting the data...")
    title = soup.title.text
    headlines = []
    paragraphs = []
    attachments = ["ul", "ol", "dl","table","img"]
    headtags = ['h2','h3']
    temp = []
    stop_words = [
    "this page",
    "please click",
    "please share",
    "comment",
    "{",
    "}",
    r"https://",
    ]

    # Identify the main section by finding where the most paragraphs are
    for p in soup.body.find_all("p", class_ = None):
        parent = p.find_parent()
        temp.append(parent)
    section = max(set(temp), key = temp.count)

    # See if the section has a class
    try:
        cls = ", class_ = '{0}'".format(" ".join(section["class"]))
    except KeyError:
        cls = ""
    # See if the section has an id
    try:
        id = ", id = '{0}'".format(section["id"])
    except KeyError:
        id = ""
    string = "find('{0}'{1}{2})".format(section.name, cls, id)

    # Specify the field of extraction
    expression = 'soup.body.{0}.find_all("p", class_ = None)'.format(string)
    locals_list = locals()
    exec('content = ' + expression, globals(), locals_list)
    content = locals_list["content"]
    attachNext = False
    # To count paragraphs that we've already checked
    count = 0
    # Organize the paragraphs and their headlines
    for Par in content:
        # Sometimes images and what not are hidden inside paragraph tags
        # Identify the paragraphs that don't have any text and get rid of them right away
        if len(Par.text) == 0:
            continue
        # Keeping track of the paragraph's number
        count += 1
        # Create a text clone
        p = Par.text

        # Check if the paragraph includes any links
        flag = 0
        for word in stop_words:
            if re.search(word, p, re.IGNORECASE):
                flag = 1
        if flag:
            continue

        # Regardless of the headtag name, find the nearest one
        h = " "
        for sibling in Par.previous_siblings:
            # Clean the NavigableString from the tags
            head = bleach.clean(str(sibling), tags=[], strip=True)
            # Skip repeated or inapropriate headlines
            if head in headlines or re.match("https://", head):
                continue
            if sibling.name in headtags:
                h = head
                break

        # See if there's an attachment in a form of another html element following the paragraphs
        attachment = None
        try:
            next = Par.next_sibling
            # Identify the type of attachment
            if next.name in attachments:
                attachment = next
            # See if there was an empty element before the attachment
            else:
                try:
                    next_next = Par.next_sibling.next_sibling
                    if next_next.name in attachments and next.name != "p":
                        attachment = next.next
                except (AttributeError, TypeError):
                    pass
        except (AttributeError, TypeError):
            pass

        # If the previous paragraph was too short it will need more text
        if attachNext:
            if h == " ":
                paragraphs[len(paragraphs)-1] = paragraphs[len(paragraphs)-1] + "\n" + p
                attachNext = False
                # Attach the attachments if there is any, before exiting the cycle
                stickAttachments(attachment, headlines, paragraphs)
                continue
            # But if it already has a headline, treat the paragraph as normally
            else:
                attachNext = False

        # See if the paragraph is just one or two sentences
        if p.count(".") < 3 and attachment == None:

            # Check if the paragraph does have a headline and still has paragraphs ahead
            if h != " " and count != len(content):
                attachNext = True
                # Go to the last code block to add the headline and the paragraph

            # If it doesn't have a headline, we simply merge it with the previous one
            elif h == " " and len(paragraphs) != 0:
                paragraphs[len(paragraphs)-1] = paragraphs[len(paragraphs)-1] + "\n" + p
                stickAttachments(attachment, headlines, paragraphs)
                continue
                # Don't go to the last code block to add the paragraph and headline

        # The last code block
        paragraphs.append(p)
        headlines.append(h)
        stickAttachments(attachment, headlines, paragraphs)

    structure = [title, headlines, paragraphs]
    return structure

# attachImages will search images to every paragraph in the yahoo images,
# download them, and add their paths to the structure as
# structure[3] = Dictionary_of_paragraphs_and_paths_to_their_images
def attachImages(article):
    print("\nSearching related images...")
    # attachImages should return a dictionary of paragraphs and attached image paths
    images = {}
    # Create a directory for the images of this presentation specifically
    folder = r"D:\Code\Works\Current\pptWizard\wizard\images"
    # Filter out all the forbidden characters from the title to make it a folder name
    folder = os.path.join(folder, formatTitle(article[0]))
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    # Set up a headless firefox browser
    options = webdriver.FirefoxOptions()
    options.set_headless()
    browser = webdriver.Firefox(firefox_options = options)
    prefix = "https://images.search.yahoo.com/"
    # Create a list for images that have alredy been downloaded
    inStock = []
    for text in article[2]:
        keywords = findKeywords(text)
        # Add formatted + spaces between the keywords
        keywords = "+".join(keywords.split())
        # Find the keywords of the title and use it for every search query
        topic = identifyTopic(article)
        # Add formatted + spaces to fit the topic into the search link
        topic = "+".join(topic.split())
        # See if the operation can be done with no errors this time
        try:
            # Choose type of images to look for
            type = "&imgty=clipart"
            # Set additional searching criteria
            criteria = "clipart"
            # Search the keywords in yahoo images
            query = "https://images.search.yahoo.com/search/images;?fr2=sb-top-images.search&p={0}+{1}+{2}&ei=UTF-8&iscqry=&fr=sfp{3}&imgsz=large".format(criteria,keywords,topic,type)
            # Get the link to the first image from the search results page
            print("\nSearching the image...")
            try:
                link = BeautifulSoup(requests.get(query).text, "lxml").find("div", id = "results").find("a")["href"]
            # If there are now div with the id "results" it means no images are found, skip it
            except AttributeError:
                print("\nNo images found.")
                images[text] = None
                continue
            # Follow the link through the headless browser
            print("\nOpening the image...")
            browser.get(prefix+link)
            # Execute every javascript on the page to load all the content
            codes = BeautifulSoup(browser.page_source, "lxml").find_all("script")
            for js in codes:
                browser.execute_script(js.text)
            # Find the img tag and it's src
            allpics = browser.find_elements_by_tag_name("img")
            image = allpics[0]
            url = image.get_attribute("src")
            # Use the keywords to name the image and save it in the specified directory
            file = "+".join(keywords.split("+"))+".jpg"
            path = os.path.join(folder,file)
            # Create a retrying loop in case the picture can't be downloaded from the first time
            retries = 0
            flag = 0
            while retries <= 1:
                try:
                    # Try downloading the image
                    print("\nDownloading the image '{}'...".format(file))
                    # These three lines must be faster than urllib.request.urlretrieve(url, path)
                    f = open(path, 'wb')
                    f.write(request.urlopen(url).read())
                    f.close()
                    # Add the paragraph and the corresponding image path to the dictionary
                    images[text] = path
                    inStock.append(url)
                    print("Downloaded successfuly.")
                    # Return the flag and break out
                    flag = 1
                    break
                # Try again in case of a TimeoutError
                except (TimeoutError, requests.exceptions.ConnectionError, urllib.error.URLError, AttributeError):
                    print("\nTimeoutError, retrying...")
                    retries += 1
                    continue
                # Handle access denial and inner library errors
                except (urllib.error.HTTPError):
                    print("\nSomething went wrong, image skipped.")
                    images[text] = None
                    break
            # If no image was retrieved after the loop, attach an empty path to the paragraph
            if not flag:
                print("\nPoor internet connection, image skipped.")
                images[text] = None
        # If something goes wrong, pass and add an empty path to the paragraph
        except (TimeoutError, TimeoutException):
            print("Can't load the image, skipped.")
            images[text] = None
            pass
    # Close the browser
    browser.close()
    return images

# A list of errors that are similar to TimeoutError but sometimes can't be handled by the exception
TimeoutErrors = [
    TimeoutError,
    requests.exceptions.ConnectionError,
    urllib3.exceptions.MaxRetryError,
    urllib3.exceptions.NewConnectionError,
    urllib.error.URLError,
    ]
detectedError = urllib.error.HTTPError

'''
1. Try to speed up the program by optimizing it in some way...
2. Handle the better table formatting
3. Limit function is not working properly
4. Use title in image search
5. Find the dominant color in all images and use as the ppt's bg color
'''
