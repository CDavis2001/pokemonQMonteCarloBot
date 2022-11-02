from poke_env.player import Player
from poke_env.environment import Battle
from poke_env.environment.pokemon import Gen8Pokemon

class MaxDamagePlanPlayer(Player):
    
    def choose_move(self, battle):
        Active = battle.active_pokemon
        OpActive = battle.opponent_active_pokemon
        
        for Type in OpActive.types:
            if Active.damage_multipler() > 1.0:
                print ("bad matchup")
                
            
        
        
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
           best_move = max(battle.available_moves, key = lambda move: move.base_power)
           return self.create_order(best_move)
       
        else:
            return self.choose_random_move(battle)
        
  
