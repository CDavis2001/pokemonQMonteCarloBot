from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon
from poke_env.environment import Move
from utility import *
import json
import numpy as np
import random

class HybridTurnSwitchPlayer(Player):
    # self, battle -> move order
    # creates a move order to send to the server
    def choose_move(self, battle):