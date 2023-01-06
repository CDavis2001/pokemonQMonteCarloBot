from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
from utility import *
import json

class QLearningPlayer(Player):
    def __init(self):
        self.previous_battle = None
    
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        # embed battle
        
        # check if 
        self.previous_battle = battle
        return None
    
    # self, battle -> observation
    # converts specific battle instance into observation
    def embed_battle(self, battle):
        # attributes we want to track
        # type matchup modifier, effective base powers
        
        active = battle.active_pokemon()
        moves = battle.avaiable_moves()
        switches = battle.available_switches()
        op_team = battle.opponent_team()
        
        observation = "{ active_pokemon : { species : "
        observation = observation + active.species + ", hp : "
        observation = observation + str(active.current_hp / active.max_hp) + " }, opponent_team : ["
        for pokemon in op_team:
            if not pokemon.fainted:
                observation = observation + "{ species : " + pokemon.species + ", ability : " + pokemon.ability + ", item : " + pokemon.item + ", hp : " + str(pokemon.current_hp / pokemon.max_hp) + "},"
        # remove last comma
        observation = observation.rstrip(observation[-1])
        observation = observation + "}"
    
        return observation
    
    # self, battle, move -> float
    
    def get_utility(self, battle, move):
        # 
        return 0
    
    # self, battlePrevious, battleCurrent -> float
    
    def calc_utility(self, battle_current):
        a = calc_utility_of_state(self.previous_battle)
        b = calc_utility_of_state(battle_current)
        return b-a
    
    