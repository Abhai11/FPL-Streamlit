import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np


class Player:
    def __init__(self, name, rank, points, last_rank, manager_id):
        self.name = name
        self.rank = int(rank)
        self.points = int(points)
        self.last_rank = int(last_rank)
        self.manager_id = manager_id

    def get_rank(self):
        return self.rank

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def get_manager_id(self):
        return self.manager_id


class Mini_League:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def get_league_name(self):
        return self.name

    def getPlayers(self):
        return self.players


class Gameweek:
    def __init__(self, name, avg_score):
        self.name = name
        self.avg_score = avg_score

    def getName(self):
        return self.name

    def getAverageScore(self):
        return self.avg_score


class Chips:
    def __init__(self, name, gw):
        self.name = name
        self.gw = gw

    def get_chip_name(self):
        return self.name

    def get_gw(self):
        return self.gw


def get_classic_league_standings(league_code):
    try:
        league_standing_api_url = f'https://fantasy.premierleague.com/api/leagues-classic/{league_code}/standings'
        league_data = requests.get(league_standing_api_url).json()
        league_name = league_data['league']['name']
        league_standings = league_data['standings']['results']

        players = []
        for standing in league_standings:
            player_data = Player(standing['entry_name'], standing['rank'],
                                 standing['total'], standing['last_rank'], standing['entry'])
            players.append(player_data)
        return Mini_League(league_name, players)
    except Exception:
        st.write('Unable to fetch league info. Verify the league id')
        return None

# Calculate total of average score for all the gameweeks


def get_average_score(gameweek_data):
    total_average = 0
    for i in gameweek_data:
        total_average = total_average + i.getAverageScore()
    return total_average

# Get gameweek data


def get_static_event_data():
    static_url = f'https://fantasy.premierleague.com/api/bootstrap-static/'
    static_data = requests.get(static_url).json()
    events = static_data['events']
    gameweek_data = []
    for event in events:
        if event['finished'] is True:
            gameweek_data.append(
                Gameweek(event['name'], int(event['average_entry_score'])))
    return gameweek_data


def get_horizontal_bar_chart(league, gw_data, player_total_scores):
    players = league.getPlayers()
    names = []
    points = []
    colors = []
    total_points = 0

    average_score = get_average_score(gw_data)
    for player in players:
        point = player.get_points()
        total_points = total_points + point
        names.append(player.get_name())
        points.append(point)
        player_total_scores.update({player.get_name(): point})
        if point > average_score:
            colors.append('green')
        elif point < average_score:
            colors.append('red')
        else:
            colors.append('blue')

    avg_league_points = total_points/len(points)
    y_pos = np.arange(len(points))
    fig, ax = plt.subplots()
    # plt.style.use('dark_background')
    ax.axvline(average_score, color='red', linewidth=1)
    ax.axvline(avg_league_points, color='blue', linewidth=1)
    plt.barh(y_pos, points, color=colors)
    plt.yticks(y_pos, names)
    return plt


st.write("""
# FPL Mini League info
""")

league_id = st.text_input('Enter your league ID: ')

if league_id is not None and league_id != '':
    league_data = get_classic_league_standings(league_id)
    if league_data is not None:
        st.write('League Name: ', league_data.get_league_name())
        st.write('Number of players: ', len(league_data.getPlayers()))
        gw_data = get_static_event_data()
        player_total_scores = {}
        plt = get_horizontal_bar_chart(
            league_data, gw_data, player_total_scores)
        st.pyplot(plt)
