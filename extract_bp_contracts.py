from bs4 import BeautifulSoup

import re
import math
import requests
import pandas as pd
from schemas.team_payroll import TeamPayroll as teampayroll
from schemas.player_contract import PlayerContract as playercontract
from models.team_payroll import TeamPayroll
from models.player_contract import PlayerContract
import concurrent.futures
from models.sqla_utils import ENGINE, BASE, get_session
from collections import defaultdict
import gspread
from oauth2client.service_account import ServiceAccountCredentials




MODELS = [PlayerContract]
team_dict = {
    'national-league': ['atlanta-braves-2', 'miami-marlins', 'new-york-mets', 'philadelphia-phillies', 'washington-nationals' ],
    'national-league-central': ['chicago-cubs', 'cincinnati-reds', 'milwaukee-brewers', 'pittsburgh-pirates', 'st-louis-cardinals'],
    'nl-west': ['arizona-diamondbacks', 'colorado-rockies', 'los-angeles-dodgers','san-diego-padres', 'san-francisco-giants'],
    'al-east': ['baltimore-orioles', 'boston-red-sox', 'toronto-blue-jays', 'new-york-yankees', 'tampa-bay-rays'],
    'american-league': ['chicago-white-sox', 'cleveland-indians', 'minnesota-twins', 'kansas-city-royals', 'detroit-tigers'],
    'al-west': ['houston-astros', 'texas-rangers', 'oakland-athletics', 'seattle-mariners', 'los-angeles-angels']
}

team_to_code = {
    'atlanta-braves-2': 'ATL', 'miami-marlins': 'MIA', 'new-york-mets': 'NYN', 'philadelphia-phillies': 'PHI', 'washington-nationals': 'WAS',
    'chicago-cubs': 'CHN', 'cincinnati-reds': 'CIN', 'milwaukee-brewers': 'MIL', 'pittsburgh-pirates': 'PIT', 'st-louis-cardinals': 'SLN',
    'arizona-diamondbacks': 'ARI', 'colorado-rockies': 'COL', 'los-angeles-dodgers':'LAN','san-diego-padres': 'SDN', 'san-francisco-giants': 'SFN',
    'baltimore-orioles': 'BAL', 'boston-red-sox': 'BOS', 'toronto-blue-jays': 'TOR', 'new-york-yankees': 'NYA', 'tampa-bay-rays' : 'TBA',
    'chicago-white-sox': 'CHA', 'cleveland-indians': 'CLE', 'minnesota-twins': 'MIN', 'kansas-city-royals' : 'KCA', 'detroit-tigers' : 'DET',
    'houston-astros': 'HOU', 'texas-rangers': 'TEX', 'oakland-athletics': 'OAK', 'seattle-mariners': 'SEA', 'los-angeles-angels': 'LAA'
}


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'PEPTradeAPP-6f666a7771dc.json', scope) # Your json file here

gc = gspread.authorize(credentials)

def get_sheets():
    sheet_links = defaultdict(dict)
    for division in team_dict.keys():
        print(division)
        for team in team_dict[division]:
            print(team)
            url = 'https://legacy.baseballprospectus.com/compensation/cots/'+ division + '/' + team + '/'
            html = requests.get(url).text
            bs = BeautifulSoup(html, 'lxml')
            tables = bs.find_all('table')

            for table in tables:
                for row in table.find_all('tr'):
                    for col in row.find_all('td'):
                        if col.get_text().isdigit():
                            year = col.get_text()
                        for link in col.find_all('a'):
                            csv_link = link.get('href')
                            csv_link = csv_link.replace('edit#gid', 'export?format=csv&gid')
                            csv_link = csv_link.replace('pubhtml', 'export?format=csv')
                            csv_link = csv_link.replace('pub?output=html', 'export?format=csv')
                            if 'export?format=csv' not in csv_link:
                                r = requests.get(csv_link)
                                url = r.url
                                slash_idx = url.rfind('/')
                                csv_link = url[:slash_idx] + '/export?format=csv'
                                # csv_link = csv_link + 
                            sheet_links[team][year] = csv_link
    return sheet_links

def get_fa_year(player_contract, time_frame, year):
    fa_years = []
    fa_years.append(player_contract['year 2'].item() == 'FA')
    fa_years.append(player_contract['year 3'].item() == 'FA')
    fa_years.append(player_contract['year 4'].item() == 'FA')
    fa_years.append(player_contract['year 5'].item() == 'FA')
    fa_idx = [i for i, x in enumerate(fa_years) if x]
    if len(fa_idx) > 0:
        fa_year = int(year) + fa_idx[0] + 1
    else:
        if '-' in time_frame:
            end_contract = time_frame.split('-')[1][:2]
            fa_year = int(end_contract) + 2000
        else:
            fa_year = int(year)
    return fa_year

def extract_data_from_sheet(sheet_link, year, team):
    url = sheet_link
    try:
        df = pd.read_csv(sheet_link, error_bad_lines=False, header=1)
        # print(df)
        df = df.iloc[:, 0:10]
        
        if len(df.columns) == 10 and df.columns[1] == "Pos'n":
            df.columns = ['player', 'pos', 'service_time', 'agent', 'terms', 'year 1', 'year 2', 'year 3', 'year 4', 'year 5']
            df = df[df['terms'].notna()]
            df = df.drop_duplicates(subset='player', keep='first')
            players = df['player'].unique()
            lengths = []
            values = []
            years = []
            for player in players:
                player_contract = df[df['player'] == player]
                terms = player_contract['terms']
                if terms.size == 1:
                    terms = terms.item()
                    # print(terms)
                    # print(isinstance(terms, str))
                    # print(terms[0:1].isdigit())
                    if isinstance(terms, str) and terms[0:1].isdigit():
                        terms = terms.split('/', 1)
                    
                        length = int(terms[0][:2])
                        try:
                            value_years = terms[1].split(' ')
                            value_dollar = value_years[0]
                            time_frame = value_years[1]
                            s_value = value_dollar.replace('$', '').replace(',', '').replace('M', '')
                            value = float(s_value)
                            if 'M' in value_dollar:
                                value *= 1000000
                            fa_year = get_fa_year(player_contract, time_frame, year)
                        except Exception as e:
                            # print('calc brok')
                            length, value, fa_year = 0, 0, int(year)
                        
                    else:
                        length,value,fa_year = 0, 0, int(year)
                else:
                    length,value,fa_year = 0, 0, int(year)
                lengths.append(length)
                values.append(value)
                years.append(fa_year)
            df['contract_length'] = lengths
            df['contract_value'] = values
            df['free_agent_year'] = years
            #print(df)
            df['team'] = team
            df['year'] = int(year)
            df = df[df['player'].notna()]
            contract_dict = df.to_dict('records')
            return contract_dict
        else:
            return None
    except Exception as e:
        print(e)
        print(sheet_link, team, year)

def load(results):
    '''
    @param results - dictionary of a list of teams to be loaded into the SQL database
    '''
    BASE.metadata.create_all(tables=[x.__table__ for x in MODELS], checkfirst=True)
    #print(results)
    session = get_session()
    for model in MODELS:
        data = results[model.__tablename__]
        print(data)
        i = 0
        # Here is where we convert directly the dictionary output of our marshmallow schema into sqlalchemy
        objs = []
        for row in data:
            print(row)
            if i % 1000 == 0:
                print('loading...', i)
            i+=1
            try:
                session.merge(model(**row))
            except Exception as e:
                print(e)
                continue
    session.commit()

sheets = get_sheets()

for team in sheets.keys():
    if team not in team_dict['national-league'] and team not in team_dict['national-league-central']:
        rows = {'PlayerContract': []}
        for year in sheets[team].keys():
            parsed_contracts = extract_data_from_sheet(sheets[team][year], year, team_to_code[team])
            if parsed_contracts is not None:
                rows['PlayerContract'].extend(playercontract(many=True).dump(parsed_contracts))
        load(rows)