from poke_env import PlayerConfiguration, ShowdownServerConfiguration
from agents.QLearningAgentLite import QLearningLitePlayer
from agents.HybridHPSwitch import HybridHPSwitchPlayer
from agents.HybridInfoSwitch import HybridInfoSwitchPlayer
from agents.HybridTurnSwitch import HybridTurnSwitchPlayer
from agents.MonteCarloAgent import MonteCarloPlayer
from agents.MaxDamagePlanAgent import MaxDamagePlanPlayer
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
    
    player = MaxDamagePlanPlayer(
        player_configuration=PlayerConfiguration("qmonte1", "Neptunium237"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )
    
    player = QLearningLitePlayer(
        player_configuration=PlayerConfiguration("qmonte2", "ProjectTest2"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )
    
    player = HybridHPSwitchPlayer(
        player_configuration=PlayerConfiguration("qmonte3", "ProjectTest3"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )
    
    player = HybridTurnSwitchPlayer(
        player_configuration=PlayerConfiguration("qmonte4", "ProjectTest4"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )
    """
    player = HybridInfoSwitchPlayer(
        player_configuration=PlayerConfiguration("qmonte5", "ProjectTest5"),
        server_configuration=ShowdownServerConfiguration,
        battle_format="gen8ou", team=team, start_timer_on_battle_start=True
    )

    # Playing 5 games on the ladder
    await player.ladder(100)

    # Print the rating of the player and its opponent after each battle
    for battle in player.battles.values():
        print(battle.rating, battle.opponent_rating)
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())