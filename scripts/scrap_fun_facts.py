#./scripts/scrap_fun_facts.py
"""
Python Script to scrap amazing fun facts.
"""

import os
import re
from typing import List
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4.element import Tag

QUOTES_FILENAME = "/funfacts.txt"
QUOTES_TXT_PATH = os.getcwd() + "/funfacts"
QUOTES_FILE_PATH = QUOTES_TXT_PATH + QUOTES_FILENAME
QUOTES_URL = "https://gotechug.com/interesting-facts-about-computers-you-didnt-know/"

def get_bs4_obj(url: str) -> BeautifulSoup:
    '''
    Get BeautifulSoup object for given QOUTES_URL.
    '''
    # See reason to use Request: https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs4Obj = BeautifulSoup(html, 'html.parser')
    return bs4Obj

def filter_p_tags(ptag: Tag) -> bool:
    '''
    Get required p tags only.
    '''
    return re.match(r"[0-9]+.", ptag.get_text())

def get_p_tags(bs4Obj: BeautifulSoup) -> List[Tag]:
    '''
    Get all p tags from the BeautifulSoup obj.

    Note: It is the requirement for given QUOTES_URL, it shall be different for different URL to scrap.
    '''
    allP = bs4Obj.find_all('p')
    allReleventP = list(filter(filter_p_tags, allP))
    return allReleventP

def get_all_facts(ptags: List[Tag]):
    '''
    Yield all facts present in p tags.
    '''
    for p in ptags:
        fact = re.sub(r"[0-9]+\. ", "", p.get_text())
        yield fact + "\n"

def save_fun_facts(ptags: List[Tag]):
    '''
    Save extracted qoutes in a text file, create a new folder if not already present
    '''
    global QUOTES_TXT_PATH, QUOTES_FILE_PATH
    if not os.path.exists(QUOTES_TXT_PATH):
        os.mkdir(QUOTES_TXT_PATH)
    
    with open(QUOTES_FILE_PATH, 'w') as file:
        for txt in get_all_facts(ptags):
            file.write(txt)
    
    print(f'All Fun Facts written to file: {QUOTES_FILE_PATH}')


if __name__ == "__main__":
    bs4Obj = get_bs4_obj(QUOTES_URL)
    allP = get_p_tags(bs4Obj)
    save_fun_facts(allP)