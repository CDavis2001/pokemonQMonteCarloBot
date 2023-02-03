from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
from poke_env.environment import Move
from utility import *
import json
import numpy as np
import random

class QLearningPlayer(Player):
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        
        # ------------------------------------------------------------------
        # Explore Exploit, exploration = 20%
        gamma = 20
        x = random.randint(1,100)
        
        if x <= gamma:
            explore = True
        else:
            explore = False
        
        # ------------------------------------------------------------------
        # Observe Current State
        observation = embed_battle(battle)
        
        # -------------------------------------------------------------------
        # Update last action taken with actual outcome utility
        if self.firstturn:
           self.firstturn = False 
        else:
            new = False
            # update previous action taken with its actual utility
            
            # calc utility gain from last action
            utility_gain = state_utility(observation) - state_utility(self.last_state)
            
            
            file = open("KB.json")
            KB = json.load(file)
            for i in range(len(KB["KB"])):
                if KB["KB"][i]["observation"] == self.last_state:
                    KB["KB"][i]["actions"][str(self.action_index)]["utility"] += utility_gain
                
            file.close()
            file = open("KB.json", "w")
            
            KB = json.dumps(KB, indent=4)
            file.write(KB)
            file.close()
            
        self.last_state = observation
        # ---------------------------------------------------------------------
        # Exploring, choose random action
        # create dict of actions
        actions = {}
        for i in range(len(battle.available_switches)):
            actions[i + len(battle.available_moves)] = {}
            actions[i + len(battle.available_moves)]["action"] = battle.available_switches[i].species + ";switch"
            actions[i + len(battle.available_moves)]["utility"] = 1    
        for i in range(len(battle.available_moves)):
            actions[i] = {}
            actions[i]["action"] = battle.available_moves[i].id + ";move"
            actions[i]["utility"] = 1
        
        
        if explore:
            options = len(battle.available_moves) + len(battle.available_switches)
            choice = random.randint(0,options-1)
            self.action_index = choice
            action = actions[choice]["action"]
            action = action.split(";")
            if action[1] == "switch":
                action = Pokemon(species=action[0])
            else:
                action = Move(move_id = action[0])
            return self.create_order(action)
        
        # -------------------------------------------------------------------
        # Exploiting
        
        file = open("KB.json")
        KB = json.load(file)
        file.close()
        
        
        
        new = True
        for i in range(len(KB["KB"])):
            if len(KB["KB"]) == 0:
                break
            if KB["KB"][i]["observation"] == observation:
                memory = KB["KB"][i]
                new = False
        
        # --------------------------------
        # Dealing with new state
        if new:
            # populate KB with new observations with actions
            file = open("KB.json", "w")
            
            
            
            
            
            # wrap actions and observations into one dict
            JSONrecord = {}
            JSONrecord['observation'] = observation
            JSONrecord['actions'] = actions
            
            KB["KB"].append(JSONrecord)
            KB = json.dumps(KB, indent=4)
            file.write(KB)
            file.close()
            # case for choosing move in new situation - either pick randomly or 
            # use similar situaiton
            
            
            options = len(battle.available_moves) + len(battle.available_switches)
            choice = random.randint(0,options-1)
            self.action_index = choice
            action = actions[choice]["action"]
            action = action.split(";")
            if action[1] == "switch":
                action = Pokemon(species=action[0])
            else:
                action = Move(move_id = action[0])
            self.pickSimSituation(observation)
            return self.create_order(action)
            
                
        # -----------------------------
        # Dealing with familiar state
        
        else:
            # choose action based on current utility
            max_util = 0
            choice = None
            for i in range(len(memory["actions"])):
                if memory["actions"][str(i)]["utility"] > max_util:
                    max_util = memory["actions"][str(i)]["utility"]
                    choice = memory["actions"][str(i)]["action"]
                    self.action_index = i
                    
            if choice == None:
                return self.choose_random_move(battle)        
            else:
                valid = False
                action = choice.split(";")
                if action[1] == "switch":
                    action = Pokemon(species=action[0])
                    for switch in battle.available_switches:
                        if switch.species == action.species:
                            valid = True
                else:
                    action = Move(move_id = action[0])
                    for move in battle._available_moves:
                        if move.id == action.id:
                            valid = True
                if valid:
                    return self.create_order(action)
                else:
                    print("default move")
                    return self.choose_default_move()
    
    
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


    def pickSimSituation(self, state):
        return ""