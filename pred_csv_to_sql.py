from models.sqla_utils import PREDICTION_ENGINE
import pandas as pd

def convert_csv_to_sql(csvfile):
    pred_df = pd.read_csv(csvfile)
    print(pred_df)
    pred_df.to_sql(
        'minor_league_batter_scores',
        con=PREDICTION_ENGINE
    )

# convert_csv_to_sql('scoring_table_mi_pitchers.csv')

def make_mlb_scores():
    query = '''SELECT * FROM predictions.milb_batter_preds
union
select * from predictions.milb_pitcher_preds
union
select * from predictions.mlb_new_preds;'''
    df = pd.read_sql(query,
    con = PREDICTION_ENGINE)

    df.to_sql(
        'mlb_final_preds',
        con= PREDICTION_ENGINE
    )
    print(df)

def make_team_code_map():
    code_map = {
        'ARI': 'ARI',
        'ATL': 'ATL',
        'BAL': 'BAL',
        'BOS': 'BOS',
        'CHC': 'CHN',
        'CIN': 'CIN',
        'CLE': 'CLE',
        'COL': 'COL',
        'CWS': 'CHA',
        'DET': 'DET',
        'HOU': 'HOU',
        'KC': 'KCA',
        'ANA': 'ANA',
        'LA': 'LAN',
        'MIA': 'MIA',
        'MIL': 'MIL',
        'MIN': 'MIN',
        'NYM': 'NYN',
        'NYY': 'NYA',
        'OAK': 'OAK',
        'PHI': 'PHI',
        'PIT': 'PIT',
        'SD': 'SDN',
        'SEA': 'SEA',
        'SF': 'SFN',
        'STL': 'SLN',
        'TB': 'TBA',
        'TEX': 'TEX',
        'TOR': 'TOR',
        'WAS': 'WAS'
    }
    code_map = {'col_1': list(code_map.keys()), 'col_2': list(code_map.values())}
    codes_df = pd.DataFrame.from_dict(code_map)
    codes_df.columns = ['minor_league_codes', 'major_league_codes']

    codes_df.to_sql(
        'team_codes',
        PREDICTION_ENGINE
    )
    print(codes_df)
# make_team_code_map()

make_mlb_scores()
#convert_csv_to_sql('scoring_major.csv')