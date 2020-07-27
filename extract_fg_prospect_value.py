from bs4 import BeautifulSoup
import requests
import pandas as pd

from models.sqla_utils import PROSPECT_ENGINE

def extract_fg_prospect_value():
    url = 'https://blogs.fangraphs.com/an-update-to-prospect-valuation/'

    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    idx = 0
    tables =  bs.find_all('table')
    table_df = pd.read_html(tables[9].prettify())[0]
    table_df.columns = ['overall', 'value', 'num_players', 'career_war_avg', 'career_war_median', 'career_war_sd', 'bust_rate', 'star_rate']
    # table_df[table_df['overall'].str.contains('POS') == True]['is_pitcher'] = False
    # table_df[table_df['overall'].str.contains('POS') == False]['is_pitcher'] = True
    table_df['is_batter'] = table_df['overall'].str.contains('POS')

    idx += 1
    table_df.to_sql(
        'overall_values',
        con=PROSPECT_ENGINE

    )
    print(table_df)
        # print(table)
        # if table:
        #     for div in table.find_all('div'):
        #         print(div)
        #         if div == 'Valuing Top-100 Prospects':
        #             print(table)
                # if table.find('div', attrs={'class':'table-title'}).get_text() == 'Valuing Top-100 Prospects':

                #     print(table)

extract_fg_prospect_value()