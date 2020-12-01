#tests/test_scrap_funfacts.py
"""
Test for scarp_funfacts.py
"""

from scripts.scrape_fun_facts import get_bs4_obj, get_p_tags, get_all_facts, filter_p_tags
import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
import re

class TestScrapFunFacts(unittest.TestCase):

    def setUp(self):

        self.html = """
            <html>
            <head></head>
            <body>
                <p>66. some text</p>
            </body>
            </html>
        """
        self.dummyurl = 'someurl.com'

    def test_get_bs4_obj(self):
        with patch('scripts.scrape_fun_facts.Request') as mockreq:
            with patch('scripts.scrape_fun_facts.urlopen') as mockurlopen:
                mockurlopen.return_value.read.return_value = self.html
                actual = get_bs4_obj(self.dummyurl)
                expected = BeautifulSoup(self.html, 'html.parser')
                self.assertEqual(expected, actual)

    def test_get_p_tags(self):
        bs4Obj = BeautifulSoup(self.html, 'html.parser')
        actual = get_p_tags(bs4Obj)
        expected = bs4Obj.find_all('p')
        self.assertEqual(expected, actual)

    def test_get_all_facts(self):
        bs4Obj = BeautifulSoup(self.html, 'html.parser')
        allp = bs4Obj.find_all('p')
        actual = list(get_all_facts(allp))
        self.assertEqual(['some text\n'], actual)

    def test_filter_p_tags(self):
        bs4Obj = BeautifulSoup(self.html, 'html.parser')
        allp = bs4Obj.find_all('p')
        actual = filter_p_tags(allp[0])
        expected = re.match(r"[0-9]+.", allp[0].get_text())
        self.assertEqual(str(expected), str(actual))


if __name__ == "__main__":
    unittest.main()
