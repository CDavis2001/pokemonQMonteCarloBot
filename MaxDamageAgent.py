from poke_env.player import Player

class MaxDamagePlayer(Player):
    
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
           best_move = max(battle.available_moves, key = lambda move: move.base_power)
           return self.create_order(best_move)
       
        else:
            return self.choose_random_move(battle)
        
  
