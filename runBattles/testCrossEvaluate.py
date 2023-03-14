import asyncio
from agents.MaxDamageAgent import MaxDamagePlayer
from agents.MaxDamagePlanAgent import MaxDamagePlanPlayer
from agents.QLearningAgent import QLearningPlayer
from agents.MonteCarloAgent import MonteCarloPlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate, RandomPlayer
from agents.RandomAgent import makeRandomPlayer

async def main():
    file = open("Teams/SpecsLelePult noswitchmoves.txt")
    team = file.read()
    file.close()
    players = []
    players.append(RandomPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(MaxDamagePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(MaxDamagePlanPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(QLearningPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(MonteCarloPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    challenges = 100
    
    
    cross_evaluation = await cross_evaluate(players,challenges)
    table = [["-"] + [p.username for p in players]]
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])
        
    print(tabulate(table))
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    