#!/usr/bin/env python

import urllib, subprocess, os.path, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import uuid

Soup = BeautifulSoup
browser = webdriver.Chrome()

# ready state for browser interaction
def readystate_complete(d):
    return d.execute_script("return document.readyState") == "complete"

# using the url from the getUrls func
# find the "good" product image
# and save it to disk.
def getImages(url, wait):
    uid = uuid.uuid4()

    browser.get(url)
    WebDriverWait(browser, wait).until(readystate_complete)

    bodyElement = browser.page_source
    document = Soup(bodyElement).find('body')
    image = document.find_all('a', class_='image-zoom')

    # for this instance we need to make sure the 
    # image has a greater len than 1 as the "good"
    # product images are the second image.
    if image and len(image) > 1:
        extension = os.path.splitext(image[1].get('href'))[1]
        subprocess.call(['touch', str(uid) + str(extension)])
        f = open(str(uid) + str(extension), 'wb')
        f.write(urllib.urlopen(image[1].get('href')).read() + '\n')
        f.close()


# starting at this url find each 
# product url and open it up.
# send the product url to the getImages func
#TODO: allow for pagination incrementing ?p=2
def getURLS(url, wait):
    browser.get(url)
    WebDriverWait(browser, wait).until(readystate_complete)

    bodyElement = browser.page_source
    document = Soup(bodyElement).find('body')

    for row in document.find_all('div', class_='item_wrap'):
        link = row.find('a', class_='product-image', href=True)
        if link:
            getImages(link.get('href'), 50)
            print(link.get('href'))
    

# try here so that we can gracefully close the 
# the browser window after either a failure or a success.
try:
    getURLS('https://shop.ccs.com/skateboards/skateboard-decks?p=2', 50)
    browser.quit() 
except:
    browser.quit()



