import pandas as pd
import pymysql
from os import walk
import time
import shutil
import getopt
import sys
from models.sqla_utils import ENGINE, DEADLINEBASE, get_session
import datetime
from extract_fangraphs import extract_fangraphs
from extract_game_data_by_year import extract_game_data_by_year, extract_roster
from schemas.player import Player as p
from models.player import Player
from schemas.team import Team as t
from models.team import Team

team_set = set(['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CHA', 'CHN', 'CIN', 'CLE', 'COL', 'DET', 'HOU',
            'KCA', 'LAN', 'MIA', 'MIL', 'MIN', 'NYA', 'NYN', 'OAK', 'PHI', 'PIT', 'SEA',
            'SFN', 'SLN', 'SDN', 'TBA', 'TEX', 'TOR', 'WAS'])


MODELS = [Player, Team]
def init(year):
    pa_query = '''select * from PlateAppearance where year = ''' + year
    game_query = '''select * from Game where year = ''' + year
    run_query = '''select * from Run where year = ''' + year
    br_query = '''select * from BaseRunningEvent where year = ''' + year
    print('plate_appearance')
    pa_start = time.time()

    # Extract the plate appearance data
    pa_data_df = pd.concat(list(pd.read_sql_query(
        pa_query,
        con=ENGINE,
        chunksize = 10000
    )))

    # Extract game data
    game_data_df = pd.concat(list(pd.read_sql_query(
        game_query,
        con=ENGINE,
        chunksize = 10000
    )))

    # Extract run data
    run_data_df = pd.concat(list(pd.read_sql_query(
        run_query,
        con=ENGINE,
        chunksize = 10000
    )))

    # Extract base running events
    br_data_df = pd.concat(list(pd.read_sql_query(
        br_query,
        con=ENGINE,
        chunksize = 10000
    )))

    return pa_data_df, game_data_df, run_data_df, br_data_df

pa_data_df, game_data_df, run_data_df, br_data_df = init('2019')

def extract_player_data_by_date(player, team, date, pa_data_df, game_data_df, run_data_df, br_data_df, woba_weights):
    '''
    convert a combination of player, plate appearance, run, and game data into team level 
    @param player - 8 character player id of player
    @param team - three letter string team code
    @param date - string of appropriate date
    @param pa_data_df - dataframe containing every plate appearance from @date
    @param player_data_df - dataframe containing player statistics
    @param run_data_df - dataframe containing info for each run scored in @date
    @param game_data_df - dataframe containing info on every game played in the season
    @param woba_weights - dataframe containing the woba weight for every batting event
    '''
    date = date.date()
    player_dict = {}
    pa_date = pa_data_df.date <= date
    game_date = game_data_df.date == date
    run_date = run_data_df.date == date
    br_date = (br_data_df.date == date) & (br_data_df.running_team == team)
    infield = set([1, 2, 3, 4, 5, 6])
    team_scored = run_data_df.scoring_team == team
    team_scored_against = run_data_df.conceding_team == team
    position = (game_data_df.starting_pitcher_home == player) | (game_data_df.starting_catcher_home == player) | (game_data_df.starting_first_home == player) | (game_data_df.starting_second_home == player) | (game_data_df.starting_third_home == player)  | (game_data_df.starting_short_home == player) | (game_data_df.starting_left_home == player) | (game_data_df.starting_right_home == player) | (game_data_df.starting_center_home == player) | (game_data_df.starting_pitcher_away == player) | (game_data_df.starting_catcher_away == player) | (game_data_df.starting_first_away == player) | (game_data_df.starting_second_away == player)| (game_data_df.starting_third_away == player) | (game_data_df.starting_short_away == player) | (game_data_df.starting_left_away == player) | (game_data_df.starting_right_away == player) | (game_data_df.starting_center_away == player)
    infield_fly = (pa_data_df.hit_loc <= 6) & ((pa_data_df.ball_type == 'F') | (pa_data_df.ball_type == 'P'))
    batter_team_bool = (pa_data_df.batter_id == player) & (pa_data_df.batter_team == team) 
    pitcher_team_bool = (pa_data_df.pitcher_id == player) & (pa_data_df.pitcher_team == team)
    player_dict['GS'] = game_data_df[position & game_date].date.count()
    player_dict['GP'] = len(pa_data_df[(pitcher_team_bool | batter_team_bool) & pa_date].game_id.unique())
    player_dict['PA'] = pa_data_df[batter_team_bool & (pa_data_df.pa_flag) & pa_date].pa_flag.count()
    player_dict['AB'] = pa_data_df[batter_team_bool & (pa_data_df.ab_flag) & pa_date].ab_flag.count()
    player_dict['S'] = pa_data_df[batter_team_bool & (pa_data_df.hit_val == 1) & pa_date].hit_val.count()
    player_dict['D'] = pa_data_df[batter_team_bool & (pa_data_df.hit_val == 2) & pa_date].hit_val.count()
    player_dict['T'] = pa_data_df[batter_team_bool & (pa_data_df.hit_val == 3) & pa_date].hit_val.count()
    player_dict['HR'] = pa_data_df[batter_team_bool & (pa_data_df.hit_val == 4) & pa_date].hit_val.count()
    player_dict['TB'] = pa_data_df[batter_team_bool & (pa_data_df.hit_val > 0) & pa_date].hit_val.sum()
    player_dict['H'] = player_dict['S'] + player_dict['D'] + player_dict['T'] + player_dict['HR']
    player_dict['R'] = run_data_df[(run_data_df.scoring_player == player) & run_date & team_scored].scoring_player.count()
    player_dict['RBI'] = pa_data_df[batter_team_bool & (pa_data_df.rbi > 0) & pa_date].rbi.sum()
    player_dict['SB'] = br_data_df[(br_data_df.runner == player) & (br_data_df.event == 'S') & br_date].runner.count()
    player_dict['CS'] = br_data_df[(br_data_df.runner == player) & (br_data_df.event == 'C') & br_date].runner.count()
    player_dict['BB'] = pa_data_df[batter_team_bool & ((pa_data_df.event_type == 14) | (pa_data_df.event_type == 15)) & pa_date].pa_flag.count()
    player_dict['IBB'] = pa_data_df[batter_team_bool & (pa_data_df.event_type == 15) & pa_date].pa_flag.count()
    player_dict['SO'] = pa_data_df[batter_team_bool & (pa_data_df.event_type == 3) & pa_date].pa_flag.count()
    player_dict['HBP'] = pa_data_df[batter_team_bool & (pa_data_df.event_type == 16) & pa_date].pa_flag.count()
    player_dict['SF'] = pa_data_df[batter_team_bool & pa_data_df.sac_fly & pa_date].pa_flag.count()
    player_dict['SH'] = pa_data_df[batter_team_bool & pa_data_df.sac_bunt & pa_date].pa_flag.count()
    if player_dict['AB'] > 0:
        player_dict['AVG'] = player_dict['H'] / player_dict['AB'] + 0.0
        player_dict['OBP'] = (player_dict['H'] + player_dict['BB'] + player_dict['HBP']) / (player_dict['AB'] + player_dict['BB'] + player_dict['HBP'] + player_dict['SF'])
        player_dict['SLG'] = player_dict['TB']/player_dict['AB']
        player_dict['OPS'] = player_dict['OBP'] + player_dict['SLG']
        bb = woba_weights.wBB * (player_dict['BB'] - player_dict['IBB'])
        hbp = (woba_weights.wHBP * player_dict['HBP'])
        hits = (woba_weights.w1B * player_dict['S']) + (woba_weights.w2B * player_dict['D']) + (woba_weights.w3B + player_dict['T']) + (woba_weights.wHR * player_dict['HR'])
        baserunning = (woba_weights.runSB * player_dict['SB']) + (woba_weights.runCS * player_dict['CS'])
        sabr_PA = (player_dict['AB'] + player_dict['BB'] + player_dict['HBP'] + player_dict['SF'])
        sabr_PA_no_IBB = sabr_PA - player_dict['IBB']
        player_dict['wOBA'] = (bb + hbp + hits + baserunning)/sabr_PA_no_IBB
        player_dict['wRAA'] = ((player_dict['wOBA'] - woba_weights.wOBA)/(woba_weights.wOBAScale)) * sabr_PA
    else:
        player_dict['AVG'], player_dict['OBP'], player_dict['SLG'], player_dict['OPS'], player_dict['wOBA'], player_dict['wRAA'] = 0, 0, 0, 0, 0, 0
    player_dict['BF'] = pa_data_df[pitcher_team_bool & pa_data_df.pa_flag & pa_date].pa_flag.count()
    player_dict['IP'] = float((pa_data_df[pitcher_team_bool & (pa_data_df.outs_on_play > 0) & pa_date].outs_on_play.sum() + 0.0)/3.0)
    player_dict['Ha'] = pa_data_df[pitcher_team_bool & (pa_data_df.hit_val>0) & pa_date].hit_val.count()
    player_dict['HRa'] = pa_data_df[pitcher_team_bool & (pa_data_df.hit_val == 4) & pa_date].hit_val.count()
    player_dict['TBa'] = pa_data_df[pitcher_team_bool & (pa_data_df.hit_val>0) & pa_date].hit_val.sum()
    player_dict['BBa'] = pa_data_df[pitcher_team_bool & ((pa_data_df.event_type == 14) | (pa_data_df.event_type == 15)) & pa_date].event_type.count()
    player_dict['IBBa'] = pa_data_df[pitcher_team_bool & (pa_data_df.event_type == 15) & pa_date].event_type.count()
    player_dict['K'] = pa_data_df[pitcher_team_bool & (pa_data_df.event_type == 3) & pa_date].event_type.count()
    player_dict['HBPa'] = pa_data_df[pitcher_team_bool & (pa_data_df.event_type == 16) & pa_date].event_type.count()
    player_dict['IFFB'] = pa_data_df[pitcher_team_bool & infield_fly & pa_date].hit_loc.count()
    player_dict['BK'] = pa_data_df[pitcher_team_bool & (pa_data_df.event_type == 11) & pa_date].event_type.count()
    player_dict['W'] = game_data_df[(player == game_data_df.winning_pitcher) & (team == game_data_df.winning_team) & game_date].winning_team.count()
    player_dict['L'] = game_data_df[(player == game_data_df.losing_pitcher) & (team == game_data_df.losing_team) & game_date].losing_team.count()
    player_dict['SV'] = game_data_df[(player == game_data_df.save) & (team == game_data_df.winning_team) & game_date].winning_team.count()
    player_dict['TR'] = run_data_df[(run_data_df.responsible_pitcher == player) & team_scored_against & run_date].responsible_pitcher.count()
    player_dict['ER'] = run_data_df[(run_data_df.responsible_pitcher == player) & team_scored_against & run_data_df.is_earned & run_date].responsible_pitcher.count()
    if player_dict['IP'] > 0:
        player_dict['RA'] = (player_dict['TR'] / player_dict['IP']) * 9
        player_dict['ERA'] = (player_dict['ER'] / player_dict['IP']) * 9
        player_dict['FIP'] = ((13 * player_dict['HRa'] + (3 * (player_dict['BBa'] + player_dict['HBPa'])) - 2 * (player_dict['K']))) / player_dict['IP']
        player_dict['iFIP'] = ((13 * player_dict['HRa'] + (3 * (player_dict['BBa'] + player_dict['HBPa'])) - 2 * (player_dict['K'] + player_dict['IFFB']))) / player_dict['IP']
    else:
        player_dict['RA'], player_dict['ERA'], player_dict['FIP'], player_dict['iFIP'] = 0,0,0,0
    
    player_dict['player_id'] = player
    player_dict['team'] = team
    player_dict['date'] = date
    player_dict['year'] = date.year
    #player_dict['player_name'] = rosters[(player, team)]['player_first_name'] + ' ' + rosters[(player, team)]['player_last_name']
    return player_dict

def extract_team_data_by_date(team, date, pa_data_df, br_data_df, game_data_df, run_data_df, woba_weights):
    '''
    convert a combination of player, plate appearance, run, and game data into team level data
    @param team - three letter string team code
    @param date - string of appropriate date
    @param pa_data_df - dataframe containing every plate appearance from @date
    @param player_data_df - dataframe containing player statistics
    @param run_data_df - dataframe containing info for each run scored in @date
    @param game_data_df - dataframe containing info on every game played in the season
    @param woba_weights - dataframe containing the woba weight for every batting event
    '''
    team_dict = {}
    date = date.date()
    game_date = (game_data_df.date <= date)
    br_runner = (br_data_df.date <= date) & (br_data_df.running_team == team)
    br_pitcher = (br_data_df.date <= date) & (br_data_df.pitching_team == team)
    pa_batter = (pa_data_df.batter_team == team) & (pa_data_df.date <= date)
    pa_pitcher = (pa_data_df.pitcher_team == team) & (pa_data_df.date <= date)
    pa_date = ((pa_data_df.pitcher_team == team) | (pa_data_df.batter_team == team)) & (pa_data_df.date == date)
    run_date = (run_data_df.date <= date)
    team_scored = run_data_df.scoring_team == team
    team_scored_against = run_data_df.conceding_team == team
    infield_fly = (pa_data_df.hit_loc <= 6) & ((pa_data_df.ball_type == 'F') | (pa_data_df.ball_type == 'P'))
    team_dict['team'] = team
    team_dict['year'] = date.year
    team_dict['date'] = date
    team_dict['W'] = game_data_df[(game_data_df.winning_team == team) & game_date].winning_team.count()
    team_dict['L'] = game_data_df[(game_data_df.losing_team == team) & game_date].losing_team.count()
    team_dict['win_pct'] = (team_dict['W']/(team_dict['W'] + team_dict['L']))
    team_dict['homeW'] = game_data_df[(game_data_df.winning_team == team) & (game_data_df.home_team == team) & game_date].home_team.count()
    team_dict['homeL'] = game_data_df[(game_data_df.losing_team == team) & (game_data_df.home_team == team) & game_date].home_team.count()
    team_dict['awayW'] = game_data_df[(game_data_df.winning_team == team) & (game_data_df.away_team == team) & game_date].away_team.count()
    team_dict['awayL'] = game_data_df[(game_data_df.losing_team == team) & (game_data_df.away_team == team) & game_date].away_team.count()
    team_dict['RS'] = game_data_df[(game_data_df.home_team == team) & game_date].home_team_runs.sum() + game_data_df[(game_data_df.away_team == team) & game_date].away_team_runs.sum()
    team_dict['RA'] = game_data_df[(game_data_df.home_team == team) & game_date].away_team_runs.sum() + game_data_df[(game_data_df.away_team == team) & game_date].home_team_runs.sum()
    team_dict['DIFF'] = team_dict['RS'] - team_dict['RA']
    team_dict['exp_win_pct'] = (1/(1 + ((team_dict['RA']/team_dict['RS'])**1.83)))
    team_dict['PA'] = pa_data_df[pa_batter & pa_data_df.pa_flag == True].pa_flag.count()
    team_dict['AB'] = pa_data_df[pa_batter & pa_data_df.ab_flag].ab_flag.count()
    team_dict['S'] = pa_data_df[pa_batter & (pa_data_df.hit_val == 1)].hit_val.count()
    team_dict['D'] = pa_data_df[pa_batter & (pa_data_df.hit_val == 2)].hit_val.count()
    team_dict['T'] = pa_data_df[pa_batter & (pa_data_df.hit_val == 3)].hit_val.count()
    team_dict['HR'] = pa_data_df[pa_batter & (pa_data_df.hit_val == 4)].hit_val.count()
    team_dict['TB'] = pa_data_df[pa_batter & (pa_data_df.hit_val >= 1)].hit_val.sum()
    team_dict['H'] = pa_data_df[pa_batter & (pa_data_df.hit_val >= 1)].hit_val.count()
    team_dict['R'] = run_data_df[run_date & run_data_df.scoring_team == team].scoring_team.count()
    team_dict['RBI'] = run_data_df[run_date & (run_data_df.scoring_team == team) & (run_data_df.is_rbi == True)].scoring_team.count()
    team_dict['SB'] = br_data_df[(br_data_df.event == 'S') & br_runner].runner.count()
    team_dict['CS'] = br_data_df[(br_data_df.event == 'C') & br_runner].runner.count()
    team_dict['BB'] = pa_data_df[((pa_data_df.event_type == 14) | (pa_data_df.event_type == 15)) & pa_batter].pa_flag.count()
    team_dict['IBB'] = pa_data_df[(pa_data_df.event_type == 15) & pa_batter].pa_flag.count()
    team_dict['SO'] = pa_data_df[(pa_data_df.event_type == 3) & pa_batter].pa_flag.count()
    team_dict['HBP'] = pa_data_df[(pa_data_df.event_type == 16) & pa_batter].pa_flag.count()
    team_dict['SF'] = pa_data_df[pa_data_df.sac_fly & pa_batter].pa_flag.count()
    team_dict['SH'] = pa_data_df[pa_data_df.sac_bunt & pa_batter].pa_flag.count()
    team_dict['AVG'] = team_dict['H'] / team_dict['AB'] + 0.0
    team_dict['OBP'] = (team_dict['H'] + team_dict['BB'] + team_dict['HBP'] + 0.0) / (team_dict['AB'] + team_dict['BB'] + team_dict['HBP'] + team_dict['SF'])
    team_dict['SLG'] = team_dict['TB'] / team_dict ['AB']
    team_dict['OPS'] = team_dict['OBP'] + team_dict['SLG']
    bb = woba_weights.wBB * (team_dict['BB'] - team_dict['IBB'])
    hbp = (woba_weights.wHBP * team_dict['HBP'])
    hits = (woba_weights.w1B * team_dict['S']) + (woba_weights.w2B * team_dict['D']) + (woba_weights.w3B + team_dict['T']) + (woba_weights.wHR * team_dict['HR'])
    baserunning = (woba_weights.runSB * team_dict['SB']) + (woba_weights.runCS * team_dict['CS'])
    sabr_PA = (team_dict['AB'] + team_dict['BB'] + team_dict['HBP'] + team_dict['SF'])
    sabr_PA_no_IBB = sabr_PA - team_dict['IBB']
    team_dict['wOBA'] = ((bb + hbp + hits + baserunning)/sabr_PA_no_IBB)
    team_dict['wRAA'] = (((team_dict['wOBA'] - woba_weights.wOBA)/(woba_weights.wOBAScale)) * sabr_PA) 
    team_dict['BF'] = pa_data_df[pa_data_df.pa_flag & pa_pitcher].pa_flag.count()
    team_dict['IP'] = float((pa_data_df[(pa_data_df.outs_on_play > 0) & pa_pitcher].outs_on_play.sum() + 0.0)/3.0)
    team_dict['Ha'] = pa_data_df[(pa_data_df.hit_val>0) & pa_pitcher].hit_val.count()
    team_dict['HRa'] = pa_data_df[(pa_data_df.hit_val == 4) & pa_pitcher].hit_val.count()
    team_dict['TBa'] = pa_data_df[(pa_data_df.hit_val>0) & pa_pitcher].hit_val.sum()
    team_dict['BBa'] = pa_data_df[((pa_data_df.event_type == 14) | (pa_data_df.event_type == 15)) & pa_pitcher].event_type.count()
    team_dict['IBBa'] = pa_data_df[(pa_data_df.event_type == 15) & pa_pitcher].event_type.count()
    team_dict['K'] = pa_data_df[(pa_data_df.event_type == 3) & pa_pitcher].event_type.count()
    team_dict['HBPa'] = pa_data_df[(pa_data_df.event_type == 16) & pa_pitcher].event_type.count()
    team_dict['IFFB'] = pa_data_df[infield_fly & pa_pitcher].hit_loc.count()
    team_dict['BK'] = pa_data_df[(pa_data_df.event_type == 11) & pa_pitcher].event_type.count()
    team_dict['TR'] = run_data_df[team_scored_against & run_date].responsible_pitcher.count()
    team_dict['ER'] = run_data_df[team_scored_against & run_data_df.is_earned & run_date].responsible_pitcher.count()
    team_dict['RAA'] = (team_dict['TR'] / team_dict['IP']) * 9
    team_dict['ERA'] = (team_dict['ER'] / team_dict['IP']) * 9
    team_dict['FIP'] = (((13 * team_dict['HRa']) + (3 * (team_dict['BBa'] + team_dict['HBPa'])) - (2 * team_dict['K']))/team_dict['IP'])
    team_dict['SpIP'] = pa_data_df[(pa_data_df.sp_flag) & pa_pitcher].outs_on_play.sum()/3
    team_dict['RpIP'] = pa_data_df[~(pa_data_df.sp_flag) & pa_pitcher].outs_on_play.sum()/3
    # print(type((run_data_df.is_sp)), type(run_data_df.conceding_team == team), type(run_data_df.is_earned), type(run_date))
    team_dict['SpER'] = run_data_df[((run_data_df.is_sp == True) & (run_data_df.conceding_team == team)) & (run_data_df.is_earned == True) & run_date].is_sp.count()
    team_dict['RpER'] = run_data_df[(run_data_df.is_sp == False) & (run_data_df.conceding_team == team) 
                                    & (run_data_df.is_earned == True) & run_date].is_sp.count()
    team_dict['SpTR'] = run_data_df[(run_data_df.is_sp == True) & (run_data_df.conceding_team == team) 
                                    & run_date].is_sp.count()
    team_dict['RpTR'] = run_data_df[(run_data_df.is_sp == False) & (run_data_df.conceding_team == team) 
                                     & run_date].is_sp.count()
    relief_hr = pa_data_df[(pa_data_df.sp_flag == False) & (pa_data_df.pitcher_team == team) & (pa_data_df.hit_val == 4) & pa_pitcher].pa_flag.count()
    relief_k = pa_data_df[(pa_data_df.sp_flag == False) & (pa_data_df.pitcher_team == team) & (pa_data_df.event_type == 3) & pa_pitcher].pa_flag.count()
    relief_bb = pa_data_df[(pa_data_df.sp_flag == False) & (pa_data_df.pitcher_team == team) & ((pa_data_df.event_type == 14) | (pa_data_df.event_type == 15)) & pa_pitcher].pa_flag.count()
    start_hr = team_dict['HRa'] - relief_hr
    start_k = team_dict['K'] - relief_k
    start_bb = (team_dict['BBa'] - team_dict['HBPa']) - relief_bb
    
    team_dict['SpERA'] = (team_dict['SpER'] / team_dict['SpIP']) * 9
    team_dict['RpERA'] = (team_dict['RpER'] / team_dict['RpIP']) * 9
    team_dict['SpFIP'] = ((13 * start_hr) + (3 * start_bb) - (2 * start_k)) / (team_dict['SpIP'])
    team_dict['RpFIP'] = ((13 * relief_hr) + (3 * relief_bb) - (2 * relief_k))/(team_dict['RpIP'])
    return team_dict

def query_player_data_by_date(date, player, team):
    year = str(date.year)
    pa_data_df, game_data_df, run_data_df, br_data_df = init(year)

    woba_df = extract_fangraphs()
    woba_weights = woba_df[woba_df.Season == int(year)]

    extract_player_data_by_date(player, team, date, pa_data_df, game_data_df, run_data_df, br_data_df, woba_weights)

def query_team_data_by_date(date, team, rosters):
    year = str(date.year)
    

    woba_df = extract_fangraphs()
    woba_weights = woba_df[woba_df.Season == int(year)]
    player_dicts = []
    for player in rosters.keys():
        print(rosters[player])
        player_dict = extract_player_data_by_date(player, team, date, pa_data_df, game_data_df, run_data_df, br_data_df, woba_weights)
        player_dict['player_name'] = rosters[player]['player_first_name'] + ' ' + rosters[player]['player_last_name']
        player_dicts.append(p().dump(player_dict))
    parsed_team = t().dump(extract_team_data_by_date(team, date, pa_data_df, br_data_df, game_data_df, run_data_df, woba_weights))
    return parsed_team, player_dicts
    

def get_rosters(year):
    rosters = {}
    roster_files = set([])
    game_files = set([])
    data_zip, data_td = extract_game_data_by_year(str(year))
    
    f = []
    for (dirpath, dirnames, filenames) in walk(data_td):
        f.extend(filenames)
        break
    shutil.rmtree(data_td)
    print(f)
    for team_file in f:
        if team_file[-4:] == '.ROS':
            print('roster', team_file)
            roster_files.add(team_file)
    
    for team in roster_files:
        rosters.update(extract_roster(team, data_zip))
    
    return rosters

def load(results):
    '''
    load all of the player data into the SQL database
    @param results - dictionary of lists of dictionaries containing all the individual player rows of data
    '''
    DEADLINEBASE.metadata.create_all(tables=[x.__table__ for x in MODELS], checkfirst=True)
    session = get_session(1)
    for model in MODELS:
        data = results[model.__tablename__]
        i = 0
        # Here is where we convert directly the dictionary output of our marshmallow schema into sqlalchemy
        objs = []
        for row in data:
            if i % 1000 == 0:
                print('loading...', i)
            i+=1
            #objs.append(model(**row))
            session.merge(model(**row))
        
        #session.bulk_save_objects(objs)
    session.commit()

def main():
    rows = {table: [] for table in ['Player', 'Team']}
    opts, args = getopt.getopt(sys.argv[1:], 'y:t:d:p:')
    team = ''
    date = datetime.datetime.strptime('2019-07-31','%Y-%m-%d')
    player = ''
    for o, a in opts:
        if o == '-t':
            team = a
        if o == '-d':
            date = datetime.datetime.strptime(a, '%Y-%m-%d')
        if o == '-p':
            player = a
    rosters = get_rosters(date.year)
    if player != '':
        query_player_data_by_date(date, player, team)
    else:
        for team in team_set:
            print(team)
            parsed_team, parsed_players = query_team_data_by_date(date, team, rosters[team])

            rows['Player'].extend(parsed_players)
            rows['Team'].append(parsed_team)
    load(rows)
#query_player_data_by_date(datetime.datetime.strptime('2019-05-01', '%Y-%m-%d'), 'harpb003', 'PHI')
start = time.time()
main()
print(time.time() - start)