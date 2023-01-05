from poke_env.environment import Battle
from poke_env.environment import Pokemon

def calcPokeMatchUpModifier(Poke1, Poke2):
    # modifier for Poke1 stab attacks on Poke 2
    modifier = 1
    modifier = modifier * Poke2.damage_multiplier(Poke1.type_1)
    if Poke1.type_2:
        modifier = modifier * Poke2.damage_multiplier(Poke1.type_2)
        
    # modifier for Poke2 stab attacks on Poke 1
    modifier = modifier * Poke1.damage_multiplier(Poke2.type_1)
    if Poke2.type_2:
        modifier = modifier * Poke1.damage_multiplier(Poke2.type_2)
    
    
def calc_utility_of_state(battle):
    utility = 0
    
    team = battle._team
    op_team = battle._opponent_team
    
    for pokmon in team:
        if not pokmon[1].fainted():
            utility += 100
    
    for pokmon in op_team:
        if pokmon[1].fainted():
            utility += 100
    
    
    
    return utility
