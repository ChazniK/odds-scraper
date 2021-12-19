import requests
from bs4 import BeautifulSoup


class Match:
    def __init__(self, sport, country, competition, date_time):
        self.sport = sport
        self.country = country
        self.competition = competition
        self.date_time = date_time


class Bet:
    def __init__(self, bet_type, bookmaker, odds):
        self.bet_type = bet_type
        self.bookmaker = bookmaker
        self.odds = odds


def get_match_data(match_header_content):
    match_sport_link = match_header_content.find('div', class_ = 'btools-match-sport').a
    match_sport_league = match_header_content.find('div', class_ = 'btools-match-league')
    match_sport_country_league = match_sport_league.find_all('a')    
    sport = match_sport_link.get('title') 
    country = match_sport_country_league[0].get('title')
    competition = match_sport_country_league[1].get('title')
    date_time = match_header_content.find('div', class_ = 'btools-match-time').span.text
    return Match(sport, country, competition, date_time)


def print_match_data(match):
    print('----------------Match info----------------------------')
    print(f'Sport: {match.sport}')
    print(f'Country: {match.country}')
    print(f'League: {match.competition}')
    print(f'Match time: {match.date_time}')
    print('------------------------------------')


def get_bet_data(match_odd):
    bet_type = match_odd.find('div', class_ = 'btools-odd-mini__header').span.text
    bookmaker_png = match_odd.find('div', class_ = 'btools-odd-mini__logo').img.get('src').split('/')[-1]
    bookmaker = bookmaker_png.split('.')[0]
    odds = match_odd.find('div', class_ = 'btools-odd-mini__value').span.text
    return Bet(bet_type, bookmaker, odds)


def print_bet_data(bet):
    print(f'Match result: {bet.bet_type}')
    print(f'Bet odds: {bet.odds}')
    print(f'Bookmaker: {bet.bookmaker}')
    print('------------------------------------')


with open('match.html', 'r') as html_file:
    content = html_file.read()
    match_bets = []
    
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_ = 'btools-match')
    for match in matches:
        match_header_content =  match.find('div', class_ = 'btools-match__header')
        newMatch = get_match_data(match_header_content)
        print_match_data(newMatch)

        match_body_contents = match.find('div', class_ = 'btools-match__body')
        match_body_competitors = match_body_contents.find('div', class_ = 'btools-match-teams')
        competitor_home = match_body_competitors.a.contents[0].strip()
        competitor_away = match_body_competitors.a.contents[2].strip()

        competitors = [('home', competitor_home), ('away', competitor_away)]
        print(f'{competitors}')
        match_bet_type = match_body_competitors.span.contents[0].strip()
        match_odds = match_body_contents.find_all('div', class_ = 'btools-odd-mini')
        for match_odd in match_odds:
            newBet = get_bet_data(match_odd)
            print_bet_data(newBet)

        print('----------------Bottom Section--------------------')
        match_expected_profit = match.find('div', class_ = 'sure-bet-cta').span.contents[0].text
        print(f'Expected profit: {match_expected_profit}')
