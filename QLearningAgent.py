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
            
            # create dict of actions
            actions = {}
            
            for i in range(len(battle.available_moves)):
                actions[i] = {}
                actions[i]["action"] = battle.available_moves[i].id + ";move"
                actions[i]["utility"] = 1
            
            for i in range(len(battle.available_switches)):
                actions[i + len(battle.available_moves)] = {}
                actions[i + len(battle.available_moves)]["action"] = battle.available_switches[i].species + ";switch"
                actions[i + len(battle.available_moves)]["utility"] = 1
            
            # wrap actions and observations into one dict
            JSONrecord = {}
            JSONrecord['observation'] = observation
            JSONrecord['actions'] = actions
            
            KB["KB"].append(JSONrecord)
            KB = json.dumps(KB, indent=4)
            file.write(KB)
            file.close()
            # return actions
        
        else:
            # choose action based on current utility
            max_util = 0
            choice = None
            for i in range(len(memory["actions"])):
                if memory["actions"][str(i)]["utility"] > max_util:
                    max_util = memory["actions"][str(i)]["utility"]
                    choice = memory["actions"][str(i)]["action"]
                    
            
        return self.choose_random_move(battle)
    
    # self, battle -> observation
    # converts specific battle instance into observation
    def embed_battle(battle):
        
        
        
        active = battle.active_pokemon
        
        # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
        hp = active.current_hp / active.max_hp
        rhp = round(hp,1)
        if rhp == 0 and hp != 0:
            rhp = 0.01
        observation = "{ 'active_pokemon' : { 'species' : '"
        observation = observation + active.species + "', 'hp' : " + str(rhp) + " }, 'team' : ["
        
        
        
        
        for pokemon in battle.team.values():
            if pokemon.active:
                continue
            else:
                hp = pokemon.current_hp / pokemon.max_hp
                rhp = round(hp,1)
                if rhp == 0 and hp != 0:
                    rhp = 0.01
                observation = observation + "{ 'species' : '" + pokemon.species + "', 'hp' : " + str(rhp) + "},"
        # remove last comma
        observation = observation.rstrip(observation[-1])
        observation = observation + "],"
        
        
        op_team = battle.opponent_team
        observation = observation + " 'opponent_team' : ["
        
        for pokemon in op_team.values():
            if pokemon.item == None:
                item = "unknown"
            else:
                item = pokemon.item
            if pokemon.ability == None:
                ability = "unknown"
            else:
                ability = pokemon.ability
            # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
            hp = pokemon.current_hp / pokemon.max_hp
            rhp = round(hp,1)
            if rhp == 0 and hp != 0:
                rhp = 0.01
            observation = observation + "{ 'species' : '" + pokemon.species + "', 'ability' : '" + ability + "', 'item' : '" + item + "', 'hp' : " + str(rhp) + "},"
        # remove last comma
        observation = observation.rstrip(observation[-1])
        observation = observation + "]}"
    
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
    
    def state_utility(self, state):
        state_value = 0
        
        state_value = state_value - (1.0 - state["active_pokemon"]["hp"])
        for pkmn in state["team"]:
            state_value = state_value - (1.0 - pkmn["hp"])
        
        for pkmn in state["opponent_team"]:
            state_value = state_value + (1.0 - pkmn["hp"])
            
        return state_value
    
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
