import asyncio
from MaxDamagePlanAgent import MaxDamagePlanPlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate
from RandomAgent import makeRandomPlayer
from QLearningAgent import QLearningPlayer
from MonteCarloAgent import MonteCarloPlayer
from QLearningAgentLite import QLearningLitePlayer
from HybridHPSwitch import HybridHPSwitchPlayer

from poke_env import PlayerConfiguration, ShowdownServerConfiguration



async def main():
    
    file = open("Teams/SpecsLelePult noswitchmoves.txt")
    team = file.read()
    file.close()
    #player = QLearningPlayer(battle_format="gen8ou",team=team)
    #player = MonteCarloPlayer(battle_format="gen8ou",team=team)
    #player = QLearningLitePlayer(battle_format="gen8ou",team=team)
    player = HybridHPSwitchPlayer(battle_format="gen8ou", team=team)
    await player.send_challenges("antroz2001", n_challenges=1)
    
    
    
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    