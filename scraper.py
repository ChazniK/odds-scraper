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
    try:
        match_sport_league = match_header_content.find('div', class_ = 'btools-match-league')
        match_sport_country_league = match_sport_league.find_all('a')    
        sport = match_header_content.find('div', class_ = 'btools-match-sport').a.get('title') 
        country = match_sport_country_league[0].get('title')
        competition = match_sport_country_league[1].get('title')
        date_time = match_header_content.find('div', class_ = 'btools-match-time').span.text
        return Match(sport, country, competition, date_time)
    except:
        print('Error parsing match data')


def get_bet_data(match_odd):
    try:
        bet_type = match_odd.find('div', class_ = 'btools-odd-mini__header').span.text
        bookmaker_png = match_odd.find('div', class_ = 'btools-odd-mini__logo').img.get('src').split('/')[-1]
        bookmaker = bookmaker_png.split('.')[0]
        odds = match_odd.find('div', class_ = 'btools-odd-mini__value').span.text
        return Bet(bet_type, bookmaker, odds)
    except:
        print('Error parsing bet data')


def get_competitor_data(match_competitor_content):
    try:
        competitor_home = match_competitor_content.a.contents[0].strip()
        competitor_away = match_competitor_content.a.contents[2].strip()
        competitors = [('home', competitor_home), ('away', competitor_away)]
        return competitors
    except:
        print('Error parsing competitor content')


def get_expected_profit(match):
    try:
        expected_profit = match.find('div', class_ = 'sure-bet-cta').span.contents[0].text
        return expected_profit
    except:
        print('Error parsing expected profit')


def print_match_data(match):
    print('----------------Match info----------------------------')
    print(f'Sport: {match.sport}')
    print(f'Country: {match.country}')
    print(f'League: {match.competition}')
    print(f'Match time: {match.date_time}')
    print('------------------------------------')


def print_bet_data(bet):
    print('----------------Bet info----------------------------')
    print(f'Match result: {bet.bet_type}')
    print(f'Bet odds: {bet.odds}')
    print(f'Bookmaker: {bet.bookmaker}')
    print('------------------------------------')


if __name__ == "__main__":
    with open('match.html', 'r') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')
        matches = soup.find_all('div', class_ = 'btools-match')
        for match in matches:
            possible_outcomes = []
            match_header_content =  match.find('div', class_ = 'btools-match__header')
            newMatch = get_match_data(match_header_content)
            match_body_contents = match.find('div', class_ = 'btools-match__body')
            match_competitor_content = match_body_contents.find('div', class_ = 'btools-match-teams')
            competitors = get_competitor_data(match_competitor_content)
            match_expected_profit = get_expected_profit(match)
            match_bet_type = match_competitor_content.span.contents[0].strip()
            match_odds = match_body_contents.find_all('div', class_ = 'btools-odd-mini')
            for match_odd in match_odds:
                newBet = get_bet_data(match_odd)
            possible_outcomes.append(newBet)    
