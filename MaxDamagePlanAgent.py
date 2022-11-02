from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment import Pokemon

class MaxDamagePlanPlayer(Player):  
    
    def choose_move(self, battle):
        
        # Have a 10% chance to act completely randomly to simulate
        # a learning agent exploring
        
        Active = battle.active_pokemon
        OpActive = battle.opponent_active_pokemon
        
        
        if Active.damage_multiplier(OpActive.type_1) > 1.0:
            print ("bad matchup")
            # switch
                
            
        
        
        # If not switching, pick the move with the highest effective
        # base power
        if battle.available_moves:
            # Finds the best move among available ones
           best_move = max(battle.available_moves, key = lambda move: move.base_power)
           return self.create_order(best_move)
       
        else:
            return self.choose_random_move(battle)
        
  
