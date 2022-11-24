from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
from utility import *

class QLearningPlayer(Player):
    
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        # embed battle
        
        # check if 
        return None
    
    # self, battle -> observation
    # converts specific battle instance into observation
    def embed_battle(self, battle):
        # attributes we want to track
        # type matchup modifier, effective base powers
        observation = []
        index = 0
        observation[index] = calcPokeMatchUpModifier(battle.active_pokemon, battle.opponent_active_pokemon)
        index+=1
        observation[index] = len(battle.available_switches())
        index+=1
        i = 0
        for move in battle.available_moves():
            base_power = move.base_power
            # check for same type attack bonus
            if move.type == battle.active_pokemon.type_1:
               base_power = base_power * 1.5
            elif battle.active_pokemon.type_2:
                if move.type == battle.active_pokemon.type_2:
                   base_power = base_power * 1.5
            base_power = base_power * battle.opponent_active_pokemon.damage_multiplier(move.type)
            observation[index + i]
            i+=1
            
        return observation
    
    # self, battle, move -> float
    def get_utility(self, battle, move):
        return 0
    
    # self, battlePrevious, battleCurrent -> float
    
    def calc_utility(self, battlePrevious, battleCurrent):
        return 0
    
    