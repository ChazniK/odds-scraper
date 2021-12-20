import unittest
from bs4 import BeautifulSoup
import scraper

with open('match.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_ = 'btools-match')


class TestScraper(unittest.TestCase):

    def test_get_match_data(self):
        match_header_content =  matches[0].find('div', class_ = 'btools-match__header')
        match = scraper.get_match_data(match_header_content)
        self.assertEqual(match.sport, 'Basketball')
        self.assertEqual(match.country, 'USA')
        self.assertEqual(match.competition, 'NBA')


    def test_get_competitor_data(self):
        match_body_content = matches[0].find('div', class_ = 'btools-match__body')
        match_competitor_content = match_body_content.find('div', class_ = 'btools-match-teams')
        competitors = scraper.get_competitor_data(match_competitor_content)
        self.assertEqual(competitors[0][0], 'home')
        self.assertEqual(competitors[0][1], 'Houston Rockets')
        self.assertEqual(competitors[1][0], 'away')
        self.assertEqual(competitors[1][1], 'Brooklyn Nets')


if __name__ == "__main__":
    unittest.main()
