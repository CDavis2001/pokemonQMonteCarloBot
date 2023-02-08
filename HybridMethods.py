from poke_env.player import Player
from MonteCarloNode import Node
from poke_env.environment import Pokemon, Move
import random
from QLearningAgentLite import QLearningLitePlayer
import json

def qchoose_move(battle):
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
    # -------------------------------------------------------------------
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
        action = actions[choice]["action"]
        action = action.split(";")
        if action[1] == "switch":
            action = Pokemon(species=action[0])
        else:
            action = Move(move_id = action[0])
        return Player.create_order(action)
        
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
        options = len(battle.available_moves) + len(battle.available_switches)
        choice = random.randint(0,options-1)
        action = actions[choice]["action"]
        action = action.split(";")
        if action[1] == "switch":
            action = Pokemon(species=action[0])
        else:
            action = Move(move_id = action[0])
        #self.pickSimSituation(observation)
        return Player.create_order(action)
            
                
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
                    
        if choice == None:
            return Player.choose_random_move(battle)        
        else:
            action = choice.split(";")
            if action[1] == "switch":
                action = Pokemon(species=action[0])
                for switch in battle.available_switches:
                    if switch.species == action.species:
                        return Player.create_order(action)
            else:
                action = Move(move_id = action[0])
                for move in battle._available_moves:
                    if move.id == action.id:
                        return Player.create_order(action)
                
            return Player.choose_default_move()