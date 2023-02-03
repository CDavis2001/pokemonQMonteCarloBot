from poke_env.environment import Battle, Pokemon, MoveCategory

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


def calcDamage(user, move, target):
    userStats = user.base_stats
    targetStats = target.base_stats
    damage = (((2 * 100) / 5) + 2) * move.base_power
    if move.category == MoveCategory["PHYSICAL"]:
        damage = damage * ((2 * userStats["atk"] + 31 + 63 + 5) / (2 * targetStats["def"] + 31+63+5))
    else:
        damage = damage * ((2 * userStats["spa"] + 31 + 63 + 5) / (2 * targetStats["spd"] + 31 + 63 + 5))                
    damage = (damage / 50) + 2
    if move.type == user.type_1:
        damage = damage * 1.5
    elif user.type_2:
        if move.type == user.type_2:
            damage = damage * 1.5
    # apply type effectiveness
    damage = damage * target.damage_multiplier(move.type)
    
    return damage
    
# self, battle -> observation
# converts specific battle instance into observation
def embed_battle(battle):       
    active = battle.active_pokemon
    # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
    hp = active.current_hp / active.max_hp
    rhp = round(hp,1)
    if rhp == 0 and hp != 0:
        rhp = 0.01
    observation = "{ 'active_pokemon' : { 'species' : '"
    observation = observation + active.species + "', 'hp' : " + str(rhp) + " }, 'team' : ["
        
        
        
        
    for pokemon in battle.team.values():
        if pokemon.active:
            continue
        else:
            hp = pokemon.current_hp / pokemon.max_hp
            rhp = round(hp,1)
            if rhp == 0 and hp != 0:
                rhp = 0.01
            observation = observation + "{ 'species' : '" + pokemon.species + "', 'hp' : " + str(rhp) + "},"
    # remove last comma
    observation = observation.rstrip(observation[-1])
    observation = observation + "],"
        
        
    op_team = battle.opponent_team
    observation = observation + " 'opponent_team' : ["
        
    for pokemon in op_team.values():
        if pokemon.item == None:
            item = "unknown"
        else:
            item = pokemon.item
        if pokemon.ability == None:
            ability = "unknown"
        else:
            ability = pokemon.ability
        if pokemon.active:
            active = "active"
        else:
            active = "not active"
        # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
        hp = pokemon.current_hp / pokemon.max_hp
        rhp = round(hp,1)
        if rhp == 0 and hp != 0:
            rhp = 0.01
        observation = observation + "{ 'species' : '" + pokemon.species + "', 'active' : '" + active + "', 'ability' : '" + ability + "', 'item' : '" + item + "', 'hp' : " + str(rhp) + "},"
    # remove last comma
    observation = observation.rstrip(observation[-1])
    observation = observation + "]}"
    
    return eval(observation)