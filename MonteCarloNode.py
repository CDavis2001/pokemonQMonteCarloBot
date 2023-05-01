import json
from poke_env.environment import Move, MoveCategory, Pokemon
from utility import calcDamage
import copy
class Node:
    def __init__(self, parent, state, action):
        self.parent = parent
        self.state = copy.deepcopy(state)
        self.action = action
        self.children = []
        self.endstate = False
        self.results = dict()
        self.results[1] = 0
        self.results[-1] = 0
        self.untried_actions = []
        
        file = open("Teams/SpecsLelePult noswitchmoves.json", "r")
        data = json.load(file)
        file.close()
        
        for i in range(6):
            if data["team"][i]["species"] == state["active_pokemon"]["species"]:
                for j in range(4):
                    
                    move = Move(data["team"][i]["moves"][j])
                    self.untried_actions.append(["use", move])
            
        for pkmn in state["team"]:
            if pkmn["hp"] > 0:
                self.untried_actions.append(["switch", pkmn["species"]])
                    
        
    
    def is_end_state(self):
        if self.state["active_pokemon"]["hp"] == 0:
            loss = True
            for pkmn in self.state["team"]:
                if pkmn["hp"] != 0:
                    loss == False
                    
            if loss:
                return -1
        
        for pkmn in self.state["opponent_team"]:
            if pkmn["hp"] != 0:
                return 0
        if self.state["opponent_active"]["hp"] == 0:
            return 1
        return 0
    
    def back_propagate(self, index):
        self.results[index] +=1
        if self.parent != None:
            self.parent.back_propagate(index)
            
    def simulate(self, action):
        opp_actions = []
        
        active_pkmn = self.state["active_pokemon"]["species"]
        active_pkmn = Pokemon(species=active_pkmn)
        
        opp_pkmn = Pokemon(species=self.state["opponent_active"]["species"])
        
        
        file = open("common_pkmn.json", "r")
        data = json.load(file)
        file.close()
        

        for pkmn in data["pokemon"]:
            if opp_pkmn.species == pkmn["name"]:
                    for move in pkmn["moves"]:
                            opp_actions.append(["use",move])

        for pkmn in self.state["opponent_team"]:
            if pkmn["hp"] != 0:
                opp_actions.append(["switch", pkmn])
        
        
        nodes = []
        for opp_action in opp_actions:
            child_state = dict()
            child_state = copy.deepcopy(self.state)
            
            
            if action[0] == "switch":
                
                
                
                
                for i in range(len(child_state["team"])):
                    if child_state["team"][i]["species"] == action[1]:
                        into = copy.deepcopy(child_state["team"][i])
                        outof = copy.deepcopy(child_state["active_pokemon"])
                        child_state["team"][i] = copy.deepcopy(outof)
                        child_state["active_pokemon"] = copy.deepcopy(into)
            
            
            
            if opp_action[0] == "switch":
                for i in range(len(child_state["opponent_team"])):
                    if child_state["opponent_team"][i]["species"] == action[1]:
                        into = copy.deepcopy(child_state["opponent_team"][i])
                        outof = copy.deepcopy(child_state["opponent_active"])
                        child_state["opponent_team"][i] = copy.deepcopy(outof)
                        child_state["opponent_active"] = copy.deepcopy(into)
                        
                        
            if action[0] == "use":
                if action[1].category == MoveCategory["STATUS"]:
                    # handle status moves
                    child_state = copy.deepcopy(self.handleStatus(child_state, action[1], False))
                    
                else:
                    damage = calcDamage(active_pkmn, action[1], opp_pkmn)
                    maxhp = opp_pkmn.base_stats['hp'] * 2 + 31 + 63 + 100 + 10
                    percentage_damage = (damage / maxhp)
                    child_state["opponent_active"]["hp"] -= percentage_damage
                    if child_state["opponent_active"]["hp"] < 0:
                        child_state["opponent_active"]["hp"] = 0
                    else:
                        child_state["opponent_active"]["hp"] = round(child_state["opponent_active"]["hp"], 1)
                        if child_state["opponent_active"]["hp"] == 0:
                            child_state["opponent_active"]["hp"] = 0.01
                    
                    
            if opp_action[0] == "use":
                moveobj = Move(opp_action[1])
                if moveobj.category == MoveCategory["STATUS"]:
                    # handle status moves
                    child_state = copy.deepcopy(self.handleStatus(child_state, moveobj, True))
                else:
                    damage = calcDamage(opp_pkmn, moveobj, active_pkmn)
                    maxhp = active_pkmn.base_stats['hp'] * 2 + 31 + 63 + 100 + 10
                    percentage_damage = (damage / maxhp)
                    child_state["active_pokemon"]["hp"] -= percentage_damage
                    
                    if child_state["active_pokemon"]["hp"] < 0:
                        child_state["active_pokemon"]["hp"] = 0
                    else:
                        child_state["active_pokemon"]["hp"] = round(child_state["active_pokemon"]["hp"], 1)
                        if child_state["active_pokemon"]["hp"] == 0:
                            child_state["active_pokemon"]["hp"] = 0.01
                
            
            
            new_node = Node(self, child_state, action)
            nodes.append(new_node)
            

            
        
        
        
        
        
        
        
        
        return nodes

    def handleStatus(self, state, move, op):
        boosts = move.self_boost
        if not boosts == None:
            if op:
                for key in boosts:
                    state["opponent_active"]["boosts"][key] += boosts[key]
            else:
                for key in boosts:
                    state["active_pokemon"]["boosts"][key] += boosts[key]
        
        if move.id == "stealthrock":
            if op:
                state["field"]["stealthrock"] = 1
            else:
                state["opfield"]["stealthrock"] = 1
        elif move.id == "spikes":
            if op:
                if state["field"]["spikes"] < 3:
                    state["field"]["spikes"] += 1
            else:
                if state["opfield"]["spikes"] < 3:
                    state["opfield"]["spikes"] += 1
        if move.id == "defog":
            state["field"]["stealthrock"] = 0
            state["opfield"]["stealthrock"] = 0
            state["field"]["spikes"] = 0
            state["opfield"]["spikes"] = 0
        return copy.deepcopy(state)
        
        
  
        
        