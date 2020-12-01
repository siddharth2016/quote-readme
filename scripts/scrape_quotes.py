#./scripts/scrap_quotes.py
"""
Python Script to scrap amazing quotes by some great computer scientists
"""

import os
from typing import List
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4.element import Tag

QUOTES_FILENAME = "/quotes.txt"
QUOTES_TXT_PATH = os.getcwd() + "/quotes"
QUOTES_FILE_PATH = QUOTES_TXT_PATH + QUOTES_FILENAME
QUOTES_URL = "http://www.devtopics.com/101-more-great-computer-quotes/"

def get_bs4_obj(url: str) -> BeautifulSoup:
    '''
    Get BeautifulSoup object for given QOUTES_URL.
    '''
    # See reason to use Request: https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs4Obj = BeautifulSoup(html, 'html.parser')
    return bs4Obj


def get_ol_tags(bs4Obj: BeautifulSoup) -> List[Tag]:
    '''
    Get all ol tags from the bs4 obj.

    Note: It is the requirement for given QUOTES_URL, it shall be different for different URL to scrap.
    '''
    allOL = bs4Obj.find_all('ol')
    allReleventOL = list(filter(lambda ol: ol.attrs.get('class')!=['commentlist'], allOL))
    return allReleventOL


def get_all_quotes(oltags: List[Tag]):
    '''
    Yield all qoutes present in OL tags.
    '''
    for ol in oltags:
        yield ol.find('li').get_text()


def save_qoutes(oltags: List[Tag]):
    '''
    Save extracted qoutes in a text file, create a new folder if not already present
    '''
    global QUOTES_TXT_PATH, QUOTES_FILE_PATH
    if not os.path.exists(QUOTES_TXT_PATH):
        os.mkdir(QUOTES_TXT_PATH)
    
    with open(QUOTES_FILE_PATH, 'w') as file:
        for txt in get_all_quotes(oltags):
            file.write(txt)
    
    print(f'All Quotes written to file: {QUOTES_FILE_PATH}')


if __name__ == "__main__":
    bs4Obj = get_bs4_obj(QUOTES_URL)
    olTags = get_ol_tags(bs4Obj)
    save_qoutes(olTags)