from poke_env.player import Player
from utility import *
from utility import teampreview as tp
from MonteCarloAgent import MonteCarloPlayer
from HybridMethods import qchoose_move
class HybridTurnSwitchPlayer(Player):
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):
        # --------------------------------------------
        # Data Collection
        file = open("final_states/HybridTurn.txt", "w")
        file.write(str(state_utility(embed_battle(battle))))
        file.close()
        # -------------------------------------------
        # method picking
        self.turn += 1
        if self.turn >= 10 and not self.switch:
            self.switch = True
            self.Player = MonteCarloPlayer()
            
        if not self.switch:
            return qchoose_move(battle)
        else:
            return self.Player.choose_move(battle=battle)
    
    def teampreview(self, battle):
        self.switch = False
        self.turn = 0
        return tp(battle)