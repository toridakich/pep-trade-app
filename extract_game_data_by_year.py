import pandas as pd
import math
import requests
import os
import shutil
import zipfile
import tempfile
import io
import numpy as np
from marshmallow import EXCLUDE

def extract_game_data_by_year(year):
    game_data_url = 'https://www.retrosheet.org/events/' + year + 'eve.zip'
    data_req = requests.get(game_data_url)
    data_td = tempfile.mkdtemp()
    data_zip = zipfile.ZipFile(io.BytesIO(data_req.content))
    data_zip.extractall(data_td)
    return data_zip, data_td

def extract_roster(file_name, data_zip):
    '''
    extracts roster from team 'team_id' with the index set to the player_id
    @ param - team_id in the form YYYY + 3 letter team code
    @ return - roster dictionary from player_ids to roster info
    '''
    
    df = pd.read_table(data_zip.open(file_name), sep = ',', 
                        error_bad_lines=False, names=['player_id', 'player_last_name', 'player_first_name', 'bats', 'throws', 'team', 'pos'])
    df = df.set_index('player_id')
    roster = df.to_dict('index')
    roster = {file_name[0:3]: roster}
    return roster