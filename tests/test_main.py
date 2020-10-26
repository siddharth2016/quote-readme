#tests/test_main.py
"""
Tests for main.py
"""

from main import get_option_list, get_text_to_display
import unittest
from unittest.mock import patch, Mock

class TestQuoteReadme(unittest.TestCase):

    def test_get_option_list(self):
        with patch('main.get_quotes') as mockquotes:
            with patch('main.get_funfacts') as mockfacts:
                with patch('main.random.shuffle') as mockshuffle:
                    mockquotes.return_value = ['quote1', 'quote2']
                    actual = get_option_list('quote')
                    self.assertEqual(['quote1', 'quote2'], actual)

                    mockfacts.return_value = ['fact1', 'fact2']
                    actual = get_option_list('funfact')
                    self.assertEqual(['fact1', 'fact2'], actual)

                    mockshuffle.return_value = ['quote1', 'quote2', 'fact1', 'fact2']
                    actual = get_option_list('both')
                    self.assertEqual(['quote1', 'quote2', 'fact1', 'fact2'], actual)

    def test_get_text_to_display(self):
        with patch('main.get_option_list') as mockoptionlist:
            with patch('main.get_quote_funfact') as mockquote:
                mockquote.return_value = 'mock quote.\n'
                actual = get_text_to_display()
                self.assertEqual('<i>❝mock quote.❞</i>', actual)

                mockquote.return_value = '\xa0mock quote.\n'
                actual = get_text_to_display()
                self.assertEqual('<i>❝ mock quote.❞</i>', actual)

            


if __name__ == "__main__":
    unittest.main()
