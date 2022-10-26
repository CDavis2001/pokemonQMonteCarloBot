import asyncio
from MaxDamageAgent import MaxDamagePlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate
from RandomAgent import makeRandomPlayer

async def main():
    players = []
    for i in range(0,1):
        players.append(makeRandomPlayer())
        maxdam = MaxDamagePlayer(battle_format = "gen8randombattle")
    players.append(maxdam)
    challenges = 10
    
    
    cross_evaluation = await cross_evaluate(players,challenges)
    table = [["-"] + [p.username for p in players]]
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])
        
    print(tabulate(table))
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    