import requests
from bs4 import BeautifulSoup


with open('match.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_ = 'btools-match')
    for match in matches:
        match_header_content =  match.find('div', class_ = 'btools-match__header')
        match_sport_link = match_header_content.find('div', class_ = 'btools-match-sport').a
        match_sport = match_sport_link.get('title')
        
        print('----------------Header Section----------------------------')
        print(f'Sport: {match_sport}')
        match_sport_league = match_header_content.find('div', class_ = 'btools-match-league')
        match_sport_country_league = match_sport_league.find_all('a')
        match_country = match_sport_country_league[0].get('title')
        match_league = match_sport_country_league[1].get('title')
        print(f'Country: {match_country}')
        print(f'League: {match_league}')
        match_time = match_header_content.find('div', class_ = 'btools-match-time').span.text
        print(f'Match time: {match_time}')
        print('------------------------------------')
        
        print('----------------Body Section--------------------')
        match_body_contents = match.find('div', class_ = 'btools-match__body')
        match_body_competitors = match_body_contents.find('div', class_ = 'btools-match-teams')
        competitor_home = match_body_competitors.a.contents[0].strip()
        competitor_away = match_body_competitors.a.contents[2].strip()
        print(f'Home competitor: {competitor_home}')
        print(f'Away competitor: {competitor_away}')
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
