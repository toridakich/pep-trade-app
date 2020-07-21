from bs4 import BeautifulSoup

import requests
import pandas as pd
from schemas.team_payroll import TeamPayroll

def get_team_name(team):
    team = team.lower().split(' ')
    team_code = team[-1].upper()
    team_name = team[:-1]
    team_name = '-'.join(team_name)[:-1]
    team_name = team_name.replace('.', '')

    return team_name, team_code

def extract_sportrac(year='2020'):
    url = 'https://www.spotrac.com/mlb/payroll/'+year

    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    # tables = bs.find_all('table')
    tables = bs.find('table')
    salary_df = pd.read_html(tables.prettify())[0]
    print(salary_df['Team'])
    payrolls = []
    contracts = []
    for team in salary_df['Team']:
        team_name,team = get_team_name(team)

        if team_name != 'leagu':
            print(team_name)
            url = 'https://www.spotrac.com/mlb/' + team_name + '/yearly/payroll/roster/'

            html = requests.get(url).text
            bs = BeautifulSoup(html, 'lxml')
            
            print(len(tables))
            num_tables = 0
            
            
            for table in bs.find_all('table'):
                if num_tables < 2:
                    if num_tables == 0:
                        payroll_df = pd.read_html(table.prettify())[0]
                        payroll_df.columns = ['Type', 'NA', 'payroll_this_year', 'payroll_next_year', 'payroll_in_two_years', 'payroll_in_three_years', 'payroll_in_four_years']
                        payroll_df[payroll_df.columns[2:]] = payroll_df[payroll_df.columns[2:]].replace('[\$,]', '', regex=True).astype(float)
                        payroll_df = payroll_df.fillna(0)
                        payroll_dict = payroll_df.to_dict('index')
                        payroll_dict[0]['team'] = team
                        payrolls.append(payroll_dict[0])
                    else:
                        contract_df = pd.read_html(table.prettify())[0]
                        print(contract_df)
                        contract_df.columns = ['name', 'age', 'pos', 'contract_this_year', 'contract_next_year', 'contract_in_two_years', 'contract_in_three_years', 'contract_in_four_years']
                        url = 'https://www.spotrac.com/mlb/' + team_name + '/contracts/'

                        html = requests.get(url).text
                        bs = BeautifulSoup(html, 'lxml')
                        tables = bs.find('table')
                        contract_term_df = pd.read_html(tables.prettify())[0]
                        contract_term_df.columns = ['name', 'pos', 'age', 'exp', 'type', 'terms', 'avg_salary', 'free_agent', 'acquired']
                        players = contract_df['name'].unique()
                        lengths = []
                        values = []
                        for player in players:
                            terms = contract_term_df[contract_term_df['name'] == player]['terms'].item()
                            terms = terms.split(',', 1)
                            length = int(terms[0][:2])
                            print(terms, length)
                            try:
                                value = float(terms[1].replace('$', '').replace(',', ''))
                            except:
                                value = 0
                            
                            lengths.append(length)
                            values.append(value)
                            print(player, length, value)
                        contract_df['contract_length'] = lengths
                        contract_df['contract_values'] = values

                        #contract_df['terms'] = contract_term_df[contract_term_df['name'] == contract_df['name']]['terms']
                        print(contract_df)
                        # contracts.append()
                num_tables += 1
            
    parsed_payrolls = TeamPayroll(many=True).dump(payrolls)

    print(parsed_payrolls)
    #print(salary_df)
    return salary_df 

extract_sportrac("2021")