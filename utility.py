from poke_env.environment import Battle, Pokemon, MoveCategory, Status, SideCondition
import copy
import numpy as np

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
    
# self, battle -> observation
# converts specific battle instance into observation
def embed_battle(battle):
    observation = dict()
    
    # Handle Active Pokemon ---------------------------------------------
    
    active = battle.active_pokemon
    # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
    hp = active.current_hp / active.max_hp
    rhp = round(hp,1)
    if rhp == 0 and hp != 0:
        rhp = 0.01
    
    pkmn = dict()
    pkmn["species"] = active.species
    pkmn["hp"] = rhp
    pkmn["status"] = getStatus(active)
    pkmn["boosts"] = active.boosts
    observation["active_pokemon"] = pkmn
    
    # Handle Team Pokemon -------------------------------------------------------
        
    team = []    
        
    for pokemon in battle.team.values():
        if pokemon.active:
            continue
        else:
            pkmn = dict()
            hp = pokemon.current_hp / pokemon.max_hp
            rhp = round(hp,1)
            if rhp == 0 and hp != 0:
                rhp = 0.01
            pkmn["species"] = pokemon.species
            pkmn["hp"] = rhp
            pkmn["status"] = getStatus(pokemon)
            team.append(copy.deepcopy(pkmn))
            
    observation["team"] = copy.deepcopy(team)
    
    # Handle Opponent Pokemon ----------------------------------------------------   
        
    op_team = battle.opponent_team
    opponent_active = dict()
    opponent_team = []
        
    for pokemon in op_team.values():
        if pokemon.item == None:
            item = "unknown"
        else:
            item = pokemon.item
        if pokemon.ability == None:
            ability = "unknown"
        else:
            ability = pokemon.ability
        
        # round hp to nearest 0.1. If rounding sets hp to 0, hp is set to 0.01 instead
        hp = pokemon.current_hp / pokemon.max_hp
        rhp = round(hp,1)
        if rhp == 0 and hp != 0:
            rhp = 0.01
            
        if pokemon.active:
            opponent_active["species"] = pokemon.species
            opponent_active["ability"] = ability
            opponent_active["item"] = item
            opponent_active["hp"] = rhp
            opponent_active["status"] = getStatus(pokemon)
            opponent_active["boosts"] = pokemon.boosts
        else:
            opponent_pkmn = dict()
            opponent_pkmn["species"] = pokemon.species
            opponent_pkmn["ability"] = ability
            opponent_pkmn["item"] = item
            opponent_pkmn["hp"] = rhp
            opponent_pkmn["status"] = getStatus(pokemon)
            opponent_team.append(copy.deepcopy(opponent_pkmn))
        
    observation["opponent_active"] = copy.deepcopy(opponent_active)
    observation["opponent_team"] = copy.deepcopy(opponent_team)
    
    
    side = battle.side_conditions
    
    field = dict()
    rocks = False
    spikes = False
    for key in side:
        if key == SideCondition["STEALTH_ROCK"]:
            field["stealthrock"] = 1
            rocks = True
        elif key == SideCondition["SPIKES"]:
            spikes = True
            field["spikes"] = side[key]
            
    if not rocks:
        field["stealthrock"] = 0
    if not spikes:
        field["spikes"] = 0
    observation["field"] = copy.deepcopy(field)
    
    opside = battle.opponent_side_conditions
    
    field = dict()
    field["stealthrock"] = 0
    field["spikes"] = 0
    if len(side) != 0:
        for key in opside:
            if key == SideCondition["STEALTH_ROCK"]:
                field["stealthrock"] = 1
            elif key == SideCondition["SPIKES"]:
                field["spikes"] = opside[key]
            
    
    observation["opfield"] = copy.deepcopy(field)
    
    return copy.deepcopy(observation)

def getStatus(pkmn):
    status = pkmn.status
    if status == Status["BRN"]:
        return "BRN"
    elif status == Status["FNT"]:
        return "FNT"
    elif status == Status["FRZ"]:
        return "FRZ"
    elif status == Status["PAR"]:
        return "PAR"
    elif status == Status["PSN"]:
        return "PSN"
    elif status == Status["SLP"]:
        return "SLP"
    elif status == Status["TOX"]:
        return "TOX"
    else:
        return "none"
    
    
def state_utility(state):
        state_value = 0
        
        active = state["active_pokemon"]
        team = state["team"]
        opactive = state["opponent_active"]
        opteam = state["opponent_team"]
        field = state["field"]
        opfield = state["opfield"]
        stats = ["accuracy", "atk", "def", "spa", "spd", "spe"]
        
        
        # active pokemon hp, status, boosts
        state_value -= (1.0 - active["hp"])
        if active["status"] != "none":
            state_value -= 0.2
        for stat in stats:
            state_value += 0.05 * active["boosts"][stat]
            
        
        # team pokemon hp, status
        for pkmn in team:
            state_value -= (1.0 - pkmn["hp"])
            if pkmn["status"] != "none":
                state_value -= 0.2
        
        # opponent active pokemon hp, status, boosts
        state_value += (1.0 - opactive["hp"])
        if opactive["status"] != "none":
            state_value += 0.2
        for stat in stats:
            state_value -= 0.1 * opactive["boosts"][stat]
        
        # opponent team pokemon hp, status
        for pkmn in opteam:
            state_value += (1.0 - pkmn["hp"])
            if pkmn["status"] != "none":
                state_value += 0.2
        state_value -= (5 - len(opteam))
        
        # field condtions
        if field["stealthrock"] == 1:
            state_value -= 0.2
        if field["spikes"] != 0:
            state_value -= (field["spikes"] * 0.1)
        
        if opfield["stealthrock"] == 1:
            state_value += 0.2
        if opfield["spikes"] != 0:
            state_value += (opfield["spikes"] * 0.1)
        
        return state_value
    
    
def teampreview(battle):
        pkmn_matchup = {}

        # For each of our pokemon
        for i, pkmn in enumerate(battle.team.values()):
            # We store their average performance against the opponent team
            pkmn_matchup[i] = np.mean([
                teampreview_performance(pkmn, opp)
                for opp in battle.opponent_team.values()
            ])

        # We sort our pokemon by performance
        ordered_mons = sorted(pkmn_matchup, key = lambda k: -pkmn_matchup[k])

        # We start with the one we consider best overall
        # We use i + 1 as python indexes start from 0
        #  but showdown's indexes start from 1
        return "/team " + ''.join([str(i + 1) for i in ordered_mons])
    
def teampreview_performance(pkmn1, pkmn2):
    # calc offensive matchup multiplier for each pokemon against the other
    pkmn1vs2 = pkmn1.damage_multiplier(pkmn2.type_1)
    if pkmn2.type_2:
        pkmn1vs2 = max(pkmn1vs2, pkmn1.damage_multiplier(pkmn2.type_2))
        
    pkmn2vs1 = pkmn2.damage_multiplier(pkmn1.type_1)
    if pkmn1.type_2:
        pkmn2vs1 = max(pkmn2vs1, pkmn2.damage_multiplier(pkmn1.type_2))
        
    # return difference 
    return pkmn2vs1 - pkmn1vs2