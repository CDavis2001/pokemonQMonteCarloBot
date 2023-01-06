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
        
        observation = QLearningPlayer.embed_battle(battle)
        KB = open("tempKB.json", "a")
        KB.write(json.dumps(observation))
        KB.write(",\n")
        KB.close()
        return self.choose_random_move(battle)
    
    # self, battle -> observation
    # converts specific battle instance into observation
    def embed_battle(battle):
        # attributes we want to track
        # type matchup modifier, effective base powers
        
        active = battle.active_pokemon
        op_team = battle.opponent_team
        
        observation = "{ 'active_pokemon' : { 'species' : '"
        observation = observation + active.species + "', 'hp' : "
        observation = observation + str(active.current_hp / active.max_hp) + " }, 'opponent_team' : ["
        for key in op_team:
            pokemon = op_team[key]
            if not pokemon.fainted:
                if pokemon.item == None:
                    item = "unknown"
                else:
                    item = pokemon.item
                if pokemon.ability == None:
                    ability = "unknown"
                else:
                    ability = pokemon.ability
                observation = observation + "{ 'species' : '" + pokemon.species + "', 'ability' : '" + ability + "', 'item' : '" + item + "', 'hp' : " + str(pokemon.current_hp / pokemon.max_hp) + "},"
        # remove last comma
        observation = observation.rstrip(observation[-1])
        observation = observation + "]}"
    
        return eval(observation)
    
    # self, battle, move -> float
    
    def get_utility(self, battle, move):
        # 
        return 0
    
    # self, battlePrevious, battleCurrent -> float
    
    def calc_utility(self, battle_current):
        a = calc_utility_of_state(self.previous_battle)
        b = calc_utility_of_state(battle_current)
        return b-a
    
    