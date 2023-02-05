from poke_env.player import Player
from poke_env.environment import Battle, Pokemon, Move, SideCondition
from utility import embed_battle as full_embed
from utility import state_utility as full_utility
import copy

import json
import numpy as np
import random

class QLearningLitePlayer(Player):
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
        observation = QLearningLitePlayer.embed_battle(battle)
        # ------------------------------------------------------------------
        # Data Collection
        file = open("final_states/QLite.txt", "w")
        file.write(str(full_utility(full_embed(battle))))
        file.close()
        # -------------------------------------------------------------------
        # Update last action taken with actual outcome utility
        if self.firstturn:
           self.firstturn = False 
        else:
            new = False
            # update previous action taken with its actual utility
            try:
                # calc utility gain from last action - our reward
                utility_gain = self.state_utility(observation) - self.state_utility(self.last_state)
            

                file = open("KBLite.json")
                KB = json.load(file)
                prev_state = None
                new_state = None
                for i in range(len(KB["KB"])):
                    if KB["KB"][i]["observation"] == self.last_state:
                        prev_state = KB["KB"][i]
                    if KB["KB"][i]["observation"] == observation:
                        new_state = KB["KB"][i]
            
                if prev_state == None:
                    pass
                else:
                    stateid = str(i) + "," + str(self.action_index)
                    # case where new state is unseen, just increment by the reward
                    if new_state == None:
                        oldreward = str(prev_state["actions"][str(self.action_index)]["utility"])
                        prev_state["actions"][str(self.action_index)]["utility"] += utility_gain
                        newreward = str(prev_state["actions"][str(self.action_index)]["utility"])
                    else:
                        actions = new_state["actions"]
                        max_util = -999
                        for action in actions:
                            if actions[action]["utility"] > max_util:
                                max_util = actions[action]["utility"]
                        oldreward = str(prev_state["actions"][str(self.action_index)]["utility"])
                        prev_state["actions"][str(self.action_index)]["utility"] += utility_gain + 0.8 * (max_util - prev_state["actions"][str(self.action_index)]["utility"])
                        newreward = str(prev_state["actions"][str(self.action_index)]["utility"])
            
                    # ---------------------------------------------
                    # Data Collection
                    file = open("qvaluetracking/QLite.txt", "a")
                    file.write(stateid + ";" + oldreward + ";" + newreward + "\n")
                    file.close()
                    # ------------------------------------------------
                    
                    
                file.close()
                file = open("KBLite.json", "w")
            
                KB = json.dumps(KB, indent=4)
                file.write(KB)
                file.close()
                
            except:
                pass    
        self.last_state = observation
        # ---------------------------------------------------------------------
        # Exploring, choose random action
        # create dict of actions
        actions = {}
        for i in range(len(battle.available_moves)):
            actions[i] = {}
            actions[i]["action"] = battle.available_moves[i].id + ";move"
            actions[i]["utility"] = 0
        for i in range(len(battle.available_switches)):
            actions[i + len(battle.available_moves)] = {}
            actions[i + len(battle.available_moves)]["action"] = battle.available_switches[i].species + ";switch"
            actions[i + len(battle.available_moves)]["utility"] = 0 
        
        
        
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
        
        file = open("KBLite.json")
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
            file = open("KBLite.json", "w")
            
            
            
            
            
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
            #self.pickSimSituation(observation)
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
                action = choice.split(";")
                if action[1] == "switch":
                    action = Pokemon(species=action[0])
                    for switch in battle.available_switches:
                        if switch.species == action.species:
                            return self.create_order(action)
                else:
                    action = Move(move_id = action[0])
                    for move in battle._available_moves:
                        if move.id == action.id:
                            return self.create_order(action)
                
                return self.choose_default_move()
    
    
    def teampreview(self, battle):
        # set up object variables
        self.firstturn = True
        self.last_state = None
        self.action_index = 0
        self.final_state = None
        
        pkmn_matchup = {}

        # For each of our pokemon
        for i, pkmn in enumerate(battle.team.values()):
            # We store their average performance against the opponent team
            pkmn_matchup[i] = np.mean([
                QLearningLitePlayer.teampreview_performance(pkmn, opp)
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


    def embed_battle(battle):
        observation = dict()
    
        # Handle Active Pokemon ---------------------------------------------
    
        active = battle.active_pokemon
        # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
        hp = active.current_hp / active.max_hp
        rhp = round(hp,1)
        if rhp == 0 and hp != 0:
            rhp = 0.01
    
        pkmn = dict()
        pkmn["species"] = active.species
        pkmn["hp"] = rhp
        pkmn["boosts"] = active.boosts
        observation["active_pokemon"] = pkmn
    
        # Handle Team Pokemon -------------------------------------------------------

        team = []    
        
        for pokemon in battle.team.values():
            if pokemon.active:
                continue
            else:
                pkmn = dict()
                hp = pokemon.current_hp / pokemon.max_hp
                pkmn["species"] = pokemon.species
                if hp == 0:
                    pkmn["faint"] = "fnt"
                else:
                    pkmn["faint"] = "not"
                team.append(copy.deepcopy(pkmn))
            
        observation["team"] = copy.deepcopy(team)
    
        # Handle Opponent Pokemon ----------------------------------------------------   
        
        op_team = battle.opponent_team
        opponent_active = dict()
        
        for pokemon in op_team.values():
        
            # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
            
            if pokemon.active:
                opponent_active["species"] = pokemon.species
                hp = pokemon.current_hp / pokemon.max_hp
                rhp = round(hp,1)
                if rhp == 0 and hp != 0:
                    rhp = 0.01
                opponent_active["hp"] = rhp
        
        
     
        
        observation["opponent_active"] = copy.deepcopy(opponent_active)
    
    
        return copy.deepcopy(observation)
    
    def state_utility(self, state):
        state_value = 0
        
        active = state["active_pokemon"]
        team = state["team"]
        opactive = state["opponent_active"]
        stats = ["accuracy", "atk", "def", "spa", "spd", "spe"]
        
        
        # active pokemon hp, status, boosts
        state_value -= (1.0 - active["hp"])
        for stat in stats:
            state_value += 0.05 * active["boosts"][stat]
            
        
        # team pokemon hp, status
        for pkmn in team:
            if pkmn["faint"] == "fnt":
                state_value -= 1
        
        # opponent active pokemon hp
        state_value += (1.0 - opactive["hp"])
        

        
        return state_value