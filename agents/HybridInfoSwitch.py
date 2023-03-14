from poke_env.player import Player
from utility import *
from utility import teampreview as tp
from agents.MonteCarloAgent import MonteCarloPlayer
from agents.HybridMethods import qchoose_move
class HybridInfoSwitchPlayer(Player):
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        # --------------------------------------------
        # Data Collection
        file = open("final_states/HybridInfo.txt", "w")
        file.write(str(state_utility(embed_battle(battle))))
        file.close()
        # -------------------------------------------
        # method picking
        if not self.switch:
            if len(battle.opponent_team) == 6:
                self.switch
                self.Player = MonteCarloPlayer()
            
        if not self.switch:
            return qchoose_move(battle)
        else:
            return self.Player.choose_move(battle=battle)
    
    def teampreview(self, battle):
        self.switch = False
        return tp(battle)