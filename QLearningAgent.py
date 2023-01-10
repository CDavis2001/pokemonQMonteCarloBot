from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
from utility import *
import json
import numpy as np

class QLearningPlayer(Player):
    def __init(self):
        # memory
        print()
    
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        # embed battle
        if self.firstturn:
           self.firstturn = False 
        else:
            new = False
            # update previous action taken with its actual utility
            file = open("KB.json")
            KB = json.load(file)
            for i in range(len(KB["KB"])):
                if KB["KB"][i]["observation"] == self.last_state:
                    KB["KB"][i]["actions"][self.action_index]["utility"] = 1
                
            file.close()
        
        self.previous_battle = battle
        
        file = open("KB.json")
        KB = json.load(file)
        file.close()
        observation = QLearningPlayer.embed_battle(battle)
        
        
        new = True
        for i in range(len(KB["KB"])):
            if len(KB["KB"]) == 0:
                break
            if KB["KB"][i]["observation"] == observation:
                memory = KB["KB"][i]
                new = False
        
        
        if new:
            # populate KB with new observations with actions
            file = open("KB.json", "w")
            KB["KB"].append(observation)
            KB = json.dumps(KB, indent=4)
            file.write(KB)
            file.close()
            # return actions
        
        else:
            # choose action based on current utility
            max_util = 0
            choice = None
            for action in memory["action"]:
                if action["utility"] > max_util:
                    max_util = action["utility"]
                    choice = action["action"]
                    
            
        return self.choose_random_move(battle)
    
    # self, battle -> observation
    # converts specific battle instance into observation
    def embed_battle(battle):
        # attributes we want to track
        # type matchup modifier, effective base powers
        
        active = battle.active_pokemon
        op_team = battle.opponent_team
        
        observation = "{ 'observation' : { 'active_pokemon' : { 'species' : '"
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
        observation = observation + "]}}"
    
        return eval(observation)
    
    # self, battle, move -> float
    
    def get_utility(self, battle, move):
        # 
        KBfile = open("KB.json", "r")
        
        
        KBfile.close()
        return 0
     
    # self, battlePrevious, battleCurrent -> float
    
    def calc_utility(self, battle_current):
        current_state = QLearningPlayer.embed_battle(battle_current)
        self.last_state
        a = calc_utility_of_state(self.previous_battle)
        b = calc_utility_of_state(battle_current)
        return b-a
    
    def teampreview(self, battle):
        # set up object variables
        self.firstturn = True
        self.last_state = None
        self.action_index = 0
        
        
        pkmn_matchup = {}

        # For each of our pokemon
        for i, pkmn in enumerate(battle.team.values()):
            # We store their average performance against the opponent team
            pkmn_matchup[i] = np.mean([
                QLearningPlayer.teampreview_performance(pkmn, opp)
                for opp in battle.opponent_team.values()
            ])

        # We sort our pokemon by performance
        ordered_mons = sorted(pkmn_matchup, key = lambda k: -pkmn_matchup[k])

        # We start with the one we consider best overall
        # We use i + 1 as python indexes start from 0
        #  but showdown's indexes start from 1
        return "/team " + ''.join([str(i + 1) for i in ordered_mons])
    
    def teampreview_performance(pkmn1, pkmn2):
        # calc offensive matchup multiplier for each pokemon against the other
        pkmn1vs2 = pkmn1.damage_multiplier(pkmn2.type_1)
        if pkmn2.type_2:
            pkmn1vs2 = max(pkmn1vs2, pkmn1.damage_multiplier(pkmn2.type_2))
        
        pkmn2vs1 = pkmn2.damage_multiplier(pkmn1.type_1)
        if pkmn1.type_2:
            pkmn2vs1 = max(pkmn2vs1, pkmn2.damage_multiplier(pkmn1.type_2))
        
        # return difference 
        return pkmn2vs1 - pkmn1vs2
