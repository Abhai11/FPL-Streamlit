import streamlit as st
import requests


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

# Get mini league data


def get_classic_league_standings(league_code):
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


st.write("""
# FPL Mini League info
""")

league_id = st.text_input('Enter your league ID: ')
league_data = get_classic_league_standings(league_id)
st.write('League Name: ', league_data.get_league_name())
