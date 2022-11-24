from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon

class QLearningPlayer(Player):
    
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        return None
    
    # self, battle -> observation
    # converts specific battle instance into generic battle class
    def embed_battle(self, battle):
        # attributes we want to track
        # type matchup modifier, effective base powers, type matchup modifiers of team mates (-1 for fainted)
        observation = []
        index = 0
        observation[index]
        return None
    
    # self, battle, move -> float
    def get_utility(self, battle, move):
        return 0
    
    # self, battlePrevious, battleCurrent -> float
    
    def calc_utility(self, battlePrevious, battleCurrent):
        return 0
    
    