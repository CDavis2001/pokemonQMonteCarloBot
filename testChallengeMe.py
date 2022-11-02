import asyncio
from MaxDamagePlanAgent import MaxDamagePlanPlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate
from RandomAgent import makeRandomPlayer

from poke_env import PlayerConfiguration, ShowdownServerConfiguration

async def main():
    player = MaxDamagePlanPlayer(battle_format="gen8randombattle")
    await player.send_challenges("antroz2001", n_challenges=1)
    
    
    
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    