from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
from poke_env.environment import Move
from utility import *
from utility import teampreview as tp
from MonteCarloAgent import MonteCarloPlayer
from HybridMethods import qchoose_move

class HybridHPSwitchPlayer(Player):
    
    
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        # --------------------------------------------
        # Data Collection
        file = open("final_states/MonteCarlo.txt", "w")
        file.write(str(state_utility(embed_battle(battle))))
        file.close()
        # -------------------------------------------
        # method picking
        if not self.switch:
            total_hp = 0
            for pkmn in battle.team.values():
                total_hp += pkmn.current_hp - pkmn.max_hp
        
            if total_hp > 3:
                self.switch = True
                self.Player = MonteCarloPlayer()
            
        if not self.switch:
            return qchoose_move(battle)
        else:
            return self.Player.choose_move(battle=battle)
    
    def teampreview(self, battle):
        self.switch = False
        return tp(battle)