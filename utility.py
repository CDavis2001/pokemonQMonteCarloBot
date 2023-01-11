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
