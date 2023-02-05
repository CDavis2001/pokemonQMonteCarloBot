from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
import numpy as np
from utility import embed_battle as full_embed
from utility import state_utility
class MaxDamagePlanPlayer(Player):  
    
    def choose_move(self, battle):
        # ------------------------------------------------------------------
        # Data Collection
        file = open("final_states/MaxDamPlan.txt", "w")
        file.write(str(state_utility(full_embed(battle))))
        file.close()
        # Have a 10% chance to act completely randomly to simulate
        # a learning agent exploring
        
        Active = battle.active_pokemon
        OpActive = battle.opponent_active_pokemon
        
        
        if Active.damage_multiplier(OpActive.type_1) > 1.0:
            # switch
            possible_switches = battle.available_switches
            modifier = 4
            switch = None
            for poke in possible_switches:
                if poke.damage_multiplier(OpActive.type_1) < modifier:
                    switch = poke
                    modifier = poke.damage_multiplier(OpActive.type_1)
            if switch != None:
                return self.create_order(switch)
        
        # If not switching, pick the move with the highest effective
        # base power
        if battle.available_moves:
            # Finds the best move among available ones
            max_power = 0
            choice = None
            for move in battle.available_moves:
                power = move.base_power
                # apply STAB
                if move.type == Active.type_1:
                    power = power * 1.5
                elif Active.type_2:
                    if move.type == Active.type_2:
                        power = power * 1.5
                # apply type effectiveness
                power = power * OpActive.damage_multiplier(move.type)
                if power > max_power:
                    max_power = power
                    choice = move
            
            if choice == None:
                return self.choose_random_move(battle)
            else:
                return self.create_order(choice)
       
        else:
            return self.choose_random_move(battle)
       
    def teampreview(self, battle):
        pkmn_matchup = {}

        # For each of our pokemon
        for i, pkmn in enumerate(battle.team.values()):
            # We store their average performance against the opponent team
            pkmn_matchup[i] = np.mean([
                MaxDamagePlanPlayer.teampreview_performance(pkmn, opp)
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
    
    
        
        
        
  
