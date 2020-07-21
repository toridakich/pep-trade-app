from bs4 import BeautifulSoup

import re
import requests
import pandas as pd
from schemas.team_payroll import TeamPayroll as teampayroll
from schemas.player_contract import PlayerContract as playercontract
from models.team_payroll import TeamPayroll
from models.player_contract import PlayerContract
import concurrent.futures
from models.sqla_utils import ENGINE, BASE, get_session
from collections import defaultdict

MODELS = [TeamPayroll, PlayerContract]

def get_team_name(team):
    team = team.lower().split(' ')
    team_code = team[-1].upper()
    team_name = team[:-1]
    team_name = '-'.join(team_name)[:-1]
    team_name = team_name.replace('.', '')

    return team_name, team_code

def get_payrolls(table, team, year):
    payroll_df = pd.read_html(table.prettify())[0]
    payroll_df.columns = ['Type', 'NA', 'payroll_this_year', 'payroll_next_year', 'payroll_in_two_years', 'payroll_in_three_years', 'payroll_in_four_years']
    payroll_df[payroll_df.columns[2:]] = payroll_df[payroll_df.columns[2:]].replace('[\$,]', '', regex=True).astype(float)
    payroll_df = payroll_df.fillna(0)
    payroll_dict = payroll_df.to_dict('index')
    payroll_dict[0]['team'] = team
    payroll_dict[0]['year'] = int(year)
    return payroll_dict[0]

def get_contracts(table, team, team_name, year):
    contract_df = pd.read_html(table.prettify())[0]
    contract_df.columns = ['player', 'age', 'pos', 'contract_this_year', 'contract_next_year', 'contract_in_two_years', 'contract_in_three_years', 'contract_in_four_years']
    url = 'https://www.spotrac.com/mlb/' + team_name + '/contracts/'

    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    tables = bs.find('table')
    if tables is not None:
        contract_term_df = pd.read_html(tables.prettify())[0]
        contract_term_df.columns = ['name', 'pos', 'age', 'exp', 'type', 'terms', 'avg_salary', 'free_agent_year', 'acquired']
        players = contract_df['player'].unique()
        lengths = []
        values = []
        years = []
        for player in players:
            player_contract = contract_term_df[contract_term_df['name'] == player]
            terms = player_contract['terms']
            fa_year = player_contract['free_agent_year'].item()
            if terms.size == 1:
                terms = terms.item()
                terms = terms.split(',', 1)
                length = int(terms[0][:2])
                try:
                    value = float(terms[1].replace('$', '').replace(',', ''))
                except:
                    value = 0
                
                lengths.append(length)
                values.append(value)
                years.append(fa_year)
            else:
                print(player)
        contract_df['contract_length'] = lengths
        contract_df['contract_value'] = values
        contract_df['free_agent_year'] = years
    else:
        contract_df['contract_length'] = 0
        contract_df['contract_value'] = 0
    
    contract_df['team'] = team
    contract_df['year'] = int(year)
    contract_dict = contract_df.to_dict('records')
    return contract_dict

def extract_team(team, year):
    team_name,team = get_team_name(team)
    data = defaultdict(list)
    if team_name != 'leagu':
        print(team_name)
        url = 'https://www.spotrac.com/mlb/' + team_name + '/yearly/payroll/roster/'

        html = requests.get(url).text
        bs = BeautifulSoup(html, 'lxml')
        
        num_tables = 0
        contract_reg = re.compile('datatable cap')
        payroll_table = bs.find('table', attrs={'class': contract_reg})
        contract_table = payroll_table.find_next('table')
        payrolls = get_payrolls(payroll_table, team, year)
        if payrolls['payroll_this_year'] is not None:
            data['payroll'] = payrolls
            data['contract'] = get_contracts(contract_table, team, team_name, year)
    else:
        return None
    return data

def extract_sportrac(year='2020'):
    rows = {table: [] for table in ['TeamPayroll', 'PlayerContract']}
    url = 'https://www.spotrac.com/mlb/payroll/'+year
    
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    # tables = bs.find_all('table')
    tables = bs.find('table')
    salary_df = pd.read_html(tables.prettify())[0]
    print(salary_df['Team'])
    payrolls = []
    contracts = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        data = [executor.submit(extract_team, team, year) for team in salary_df['Team']]
        for parsed_data in concurrent.futures.as_completed(data):
            parsed_data = parsed_data.result()
            #print(parsed_data['payroll']['team'])
            if parsed_data is not None:
                print(parsed_data['payroll']['year'])
                payrolls.append(teampayroll().dump(parsed_data['payroll']))
                contracts.extend(playercontract(many=True).dump(parsed_data['contract']))
            # payrolls.append(parsed_data['payroll'])
            # contracts.extend(parsed_data['contract'])
            
    # print(payrolls)
    # parsed_payrolls = teampayroll(many=True).dump(payrolls)
    # parsed_contracts = playercontract(many=True).dump(contracts)
    rows['TeamPayroll'] = payrolls
    rows['PlayerContract'] = contracts
    #print(salary_df)
    return rows

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
            session.merge(model(**row))
    session.commit()

if __name__ == '__main__':
    rows = extract_sportrac("2020")
    load(rows)