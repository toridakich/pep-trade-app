from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import lxml
import time
import re
import math

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from models.sqla_utils import ENGINE, PROSPECTBASE, get_session

from schemas.prospect import Prospect as p
from models.prospect import Prospect
MODELS = [Prospect]


def extract_yearly_links():
    url = 'https://www.mlb.com/prospects/top100/'
    
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')

    year_dropdown = bs.find('select')
    links = []
    for option in year_dropdown.find_all('option'):
        value = option.get('value')
        if value == '2020':
            value = url
        links.append(value)
    return links
    # for select in bs.find_all('select'):
    #     print(select)

def get_name_and_rank(name_rank):
    print(name_rank)
    player_dict = {}
    items = name_rank.split('|')
    player_dict['name'] = items[0].strip()
    player_dict['team_rank'] = int(items[1].split(':')[1][:3])
    return player_dict

def handle_drafted(drafted):
    print('drafted', drafted)
    drafted = drafted.strip()
    player_dict = {}
    year_pick = drafted.split(',')
    if year_pick[0].isdigit():
        player_dict['draft_year'] = int(year_pick[0])
    else:
        return {}
    round_pick = year_pick[1].split('(')
    try:
        player_dict['draft_pos'] = int(round_pick[1].split(')')[0])
    except ValueError as e:
        print(e)
        pos = re.search(r'(\d+)', round_pick[1].split(')')[0])
        player_dict['draft_pos'] = int(pos.group(1))
    round = re.search(r'(\d+)', round_pick[0])
    # round = re.search(r'^\d', round_pick[0])
    # dig = re.search(r'\d', round_pick[0])
    if round:
        player_dict['draft_round'] = int(round.group(1))
    else:
        player_dict['draft_round'] = math.ceil(player_dict['draft_pos'] / 30)
    print('draftedplayerdict', player_dict)
    return player_dict

def handle_prospect_ranks(ranks):
    player_dict = {}
    ranks = ranks.split(',')
    for rank in ranks:
        if 'Top 100 Prospects' in rank:
            mlb_rank = int(rank.split('#')[1].split(')')[0])
            player_dict['mlb_rank'] = mlb_rank
    return player_dict

def handle_grades(grades):
    player_dict = {}
    indv_grades = grades.split('|')
    for indv_grade in indv_grades:
        indv_grade = indv_grade.strip()
        attr_val = indv_grade.split(':')
        if len(attr_val) > 1:
            player_dict[attr_val[0]] = attr_val[1]
        else:
            print(indv_grade, attr_val)
        
    if 'Overall' not in player_dict.keys():
        return {}
    return player_dict

def read_card_data(card, team):
    print(card)
    html = card.get_attribute('outerHTML')

    bs = BeautifulSoup(html, 'lxml')
    name_rank = bs.find('h3')

    if name_rank:
        name_rank = name_rank.get_text()
        player_dict = get_name_and_rank(name_rank)
    else:
        return {}
    player_dict['ml_team'] = team.upper()
    details = bs.find('div', attrs={'id': 'player-details'})

    for span in details.find_all('span'):
        is_key=True
        for innerspan in span.find_all('span'):
            dict_val = innerspan.get_text().split(':')
            if len(dict_val) > 1:
                player_dict[dict_val[0]] = dict_val[1].strip()
            # if is_key:
            #     key = innerspan.get_text()
            # else:
            #     value = innerspan.get_text()
            #     player_dict[key] = value
            # is_key = not is_key

    del player_dict['Bats']
    del player_dict['Height']
    player_dict['Age'] = int(player_dict['Age'][:2])
    if player_dict.get('Drafted') != None:
        player_dict.update(handle_drafted(player_dict['Drafted']))
    else:
        player_dict['draft_year'], player_dict['draft_round'], player_dict['draft_pos'] = None, None, None
    if player_dict.get('Other Lists') != None:
        player_dict.update(handle_prospect_ranks(player_dict['Other Lists']))
    
    blurb = bs.find('div', attrs={'class': 'player-blurb'})
    grades = blurb.find('p')

    if grades:
        if 'WATCH' in grades:
            grades = grades.find_next('p')
            if not grades:
                return player_dict
        if grades.find('b'):
            player_dict.update(handle_grades(grades.get_text().replace('Scouting grades:', '')))
        
        else:
            grades = blurb.get_text().splitlines()[0].strip()
            player_dict.update(handle_grades(grades.replace('Scouting grades:', '')))
    print(player_dict)
    return player_dict

# def etl_players_version_1(link):



def etl_team_version_2(link, team):
    print('yo')
    url = link + '?list=' + team
    year_str = re.search(r'(\d+)', link)
    year = int(year_str.group(1))
    if year == 2019 or year == 2018 or year == 2017:
        return
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    cards = driver.find_elements_by_tag_name('li')
    print(len(cards))
    player_dicts = []
    for li in cards:
        #print ii.tag_name
        try:
            # Tries to click an element
            if li.is_displayed():
                li.click()
                time.sleep(2)
                card = driver.find_elements_by_id('card-details')[0]
                try:
                    prospect = read_card_data(card, team)
                    prospect['year'] = year
                    player_dicts.append(p().dump(prospect))
                except Exception as e:
                    print(e)
                try:
                    driver.find_element_by_css_selector(".fancybox-item[title='Close']").send_keys(Keys.RETURN)
                except NoSuchElementException as e:
                    print(e)
                    time.sleep(4)
                    driver.find_element_by_css_selector(".fancybox-item[title='Close']").click()
            else:
                time.sleep(3)
                driver.find_element_by_css_selector(".fancybox-item[title='Close']").click()
                time.sleep(2)
                li.click()
            
        except ElementClickInterceptedException:
            # If pop-up overlay appears, click the X button to close
            driver.find_element_by_css_selector(".fancybox-item[title='Close']").send_keys(Keys.RETURN)
            time.sleep(3)
            li.click()
        
        except NoSuchElementException:
            
            time.sleep(3)
            try :
                driver.find_element_by_css_selector(".fancybox-item[title='Close']").send_keys(Keys.RETURN)
            except:
                pass
            li.click()
        
        time.sleep(3)

    return player_dicts


def get_version_1_player(driver):
    player_dict = {}
    headers = driver.find_elements_by_class_name('header')
    done_header = False
    for header in headers:
        if done_header:
            break
        html_header = header.get_attribute('innerHTML')
        bs = BeautifulSoup(html_header, 'lxml')
        for attr in bs.find_all('div'):
            if attr.get('class'):
                key = attr.get('class')[0]
                value = attr.get_text()
                if key == 'draft':
                    if ':' in value:
                        value = value.split(':')[1]
                    player_dict.update(handle_drafted(value))
                elif key == 'position' or key == 'rank':
                    value = value.split(':')[1]
                    if key == 'rank':
                        value = value.split('(')[0]
                elif key == 'year':
                    key = 'ETA'
                    if ':' in value:
                        value = value.split(':')[1]
                player_dict[key] = value
                done_header = True
    print(player_dict)
    # attributes = header.find_elements_by_xpath('.//div')
    # print('attributes', attributes)
    # for attr in attributes:
    #     print(attr.get_attribute('innerHTML'))

def etl_version_1_link(link):
    print('version 1')
    rows = {}


    driver=webdriver.Chrome()
    driver.get(link)
    time.sleep(3)

    players = driver.find_elements_by_class_name('player')


    for player in players:
        if player.is_displayed():
            player.click()
            time.sleep(2)
            get_version_1_player(driver)
        #print(player.get_attribute('outerHTML'))
    print(players)


    return

def etl_version_2_link(link):
    rows = {}

    html = requests.get(link).text
    bs = BeautifulSoup(html, 'lxml')
    for select in bs.find_all('select'):
        option = select.find('option')
        if option.get_text() == '30 by Team':
            for team in option.find_all_next('option'):
                print(team)
                #if team.get('value') not in set(['ari', 'atl', 'ana', 'bal', 'bos', 'chc', 'cin', 'cws', 'cle']):
                rows['Prospect'] = []
                prospects = etl_team_version_2(link, team.get('value'))
                if prospects:
                    rows['Prospect'].extend(prospects)
                load(rows)
    print('version 2')
    return rows

def etl_version_3_link(link):
    print('version 3')
    return


def etl_links(links):
    for link in links:
        print(link)
        if 'mlb.mlb.com' in link:
            etl_version_1_link(link)
        elif 'm.mlb.com' in link:
            load(etl_version_2_link(link))
        else:
            etl_version_3_link(link)

def load(results):
    PROSPECTBASE.metadata.create_all(tables=[x.__table__ for x in MODELS], checkfirst=True)
    #print(results)
    session = get_session(3)
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

links = extract_yearly_links()
etl_links(links)





