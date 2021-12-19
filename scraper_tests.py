import unittest
import scraper


class TestMain(unittest.TestCase):

    with open('match.html', 'r') as html_file:

    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_ = 'btools-match')


