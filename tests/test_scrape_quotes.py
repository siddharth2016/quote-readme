#tests/test_scrap_quotes.py
"""
Test for scrap_quotes.py
"""

from scripts.scrape_quotes import get_bs4_obj, get_ol_tags, get_all_quotes
import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup

class TestScrapQuotes(unittest.TestCase):

    def setUp(self):

        self.html = """
            <html>
            <head></head>
            <body>
                <ol>
                <li>some text</li>
                </ol>
            </body>
            </html>
        """
        self.dummyurl = 'someurl.com'

    def test_get_bs4_obj(self):
        with patch('scripts.scrape_quotes.Request') as mockreq:
            with patch('scripts.scrape_quotes.urlopen') as mockurlopen:
                mockurlopen.return_value.read.return_value = self.html
                actual = get_bs4_obj(self.dummyurl)
                expected = BeautifulSoup(self.html, 'html.parser')
                self.assertEqual(expected, actual)

    def test_get_ol_tags(self):
        bs4Obj = BeautifulSoup(self.html, 'html.parser')
        actual = get_ol_tags(bs4Obj)
        expected = bs4Obj.find_all('ol')
        self.assertEqual(expected, actual)

    def test_get_all_quotes(self):
        bs4Obj = BeautifulSoup(self.html, 'html.parser')
        ollist = bs4Obj.find_all('ol')
        actual = list(get_all_quotes(ollist))
        self.assertEqual(['some text'], actual)


if __name__ == "__main__":
    unittest.main()
