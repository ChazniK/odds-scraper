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

with open('match.html', 'r') as html_file:
    content = html_file.read()
    match_bets = []
    
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_ = 'btools-match')
    for match in matches:
        match_header_content =  match.find('div', class_ = 'btools-match__header')
        match_sport_link = match_header_content.find('div', class_ = 'btools-match-sport').a
        sport = match_sport_link.get('title') 
        match_sport_league = match_header_content.find('div', class_ = 'btools-match-league')
        match_sport_country_league = match_sport_league.find_all('a')
        country = match_sport_country_league[0].get('title')
        competition = match_sport_country_league[1].get('title')
        date_time = match_header_content.find('div', class_ = 'btools-match-time').span.text

        newMatch = Match(sport, country, competition, date_time)
        print('----------------Header Section----------------------------')
        print(f'Sport: {newMatch.sport}')
        print(f'Country: {newMatch.country}')
        print(f'League: {newMatch.competition}')
        print(f'Match time: {newMatch.date_time}')
        print('------------------------------------')

        print('----------------Body Section--------------------')
        match_body_contents = match.find('div', class_ = 'btools-match__body')
        match_body_competitors = match_body_contents.find('div', class_ = 'btools-match-teams')
        competitor_home = match_body_competitors.a.contents[0].strip()
        competitor_away = match_body_competitors.a.contents[2].strip()

        competitors = [('home', competitor_home), ('away', competitor_away)]
        print(f'{competitors}')
        match_bet_type = match_body_competitors.span.contents[0].strip()
        match_odds = match_body_contents.find_all('div', class_ = 'btools-odd-mini')
        for match_odd in match_odds:
            match_odd_result = match_odd.find('div', class_ = 'btools-odd-mini__header').span.text
            match_odd_value = match_odd.find('div', class_ = 'btools-odd-mini__value').span.text
            match_odd_bookmaker_png = match_odd.find('div', class_ = 'btools-odd-mini__logo').img.get('src').split('/')[-1]
            match_odd_bookmaker = match_odd_bookmaker_png.split('.')[0]
            print(f'Match result: {match_odd_result}')
            print(f'Bet odds: {match_odd_value}')
            print(f'Bookmaker: {match_odd_bookmaker}')
            print('------------------------------------')

        print('----------------Bottom Section--------------------')
        match_expected_profit = match.find('div', class_ = 'sure-bet-cta').span.contents[0].text
        print(f'Expected profit: {match_expected_profit}')
