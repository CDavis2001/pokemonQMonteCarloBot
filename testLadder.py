from poke_env import PlayerConfiguration, ShowdownServerConfiguration
from QLearningAgentLite import QLearningLitePlayer
from HybridHPSwitch import HybridHPSwitchPlayer
from HybridInfoSwitch import HybridInfoSwitchPlayer
from HybridTurnSwitch import HybridTurnSwitchPlayer
from MonteCarloAgent import MonteCarloPlayer
from MaxDamagePlanAgent import MaxDamagePlanPlayer
import asyncio

async def main():
    
    file = open("Teams/SpecsLelePult noswitchmoves.txt")
    team = file.read()
    file.close()
    
    """
    player = MonteCarloPlayer(
        player_configuration=PlayerConfiguration("qmonte", "Neptunium237"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )
    """
    player = MaxDamagePlanPlayer(
        player_configuration=PlayerConfiguration("qmonte1", "Neptunium237"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )
    # Playing 5 games on the ladder
    await player.ladder(5)

    # Print the rating of the player and its opponent after each battle
    for battle in player.battles.values():
        print(battle.rating, battle.opponent_rating)
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())