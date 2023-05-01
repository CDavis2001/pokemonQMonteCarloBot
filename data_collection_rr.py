import asyncio
from MaxDamageAgent import MaxDamagePlayer
from MaxDamagePlanAgent import MaxDamagePlanPlayer
from QLearningAgent import QLearningPlayer
from MonteCarloAgent import MonteCarloPlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate, RandomPlayer
from QLearningAgentLite import QLearningLitePlayer
from HybridHPSwitch import HybridHPSwitchPlayer
from HybridInfoSwitch import HybridInfoSwitchPlayer
from HybridTurnSwitch import HybridTurnSwitchPlayer
from test1v1 import onev1_evaluate

# Method to get the results from a single battle between specified agents

async def getResults(players, files):
    

    cross_evaluation = await onev1_evaluate(players, 1)
    states = []
    for path in files:
        states.append(open(path))
    file = open("results/results.txt", "a")
    utility = []
    for state in states:
        utility.append(float(state.read()))
        state.close()
    for key in cross_evaluation:
        if cross_evaluation[key][0] == 0:
            file.write("LOSS;" + key + ";" + str(max(utility)) + "\n")
        else:
            file.write("WIN;" + key + ";" + str(max(utility)) + "\n")
    file.close()

async def main():
    
    # set this value for number of battles for each pair
    iterations = 1000
    
    file = open("Teams/SpecsLelePult noswitchmoves.txt")
    team = file.read()
    file.close()
    
    # Instantiate agents with the loaded teams
    
    MD = MaxDamagePlanPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True)
    MC = MonteCarloPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1)
    Q = QLearningLitePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1)
    Turn = HybridTurnSwitchPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1)
    Info = HybridInfoSwitchPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1)
    HP = HybridHPSwitchPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1)

    # simulate battle for each pairs
    for i in range(iterations):
        players = []
        players.clear()
        players = [Turn, MD]
        files = ["final_states/HybridTurn.txt", "final_states/MaxDamPlan.txt"]
        await getResults(players, files)
        
        players.clear()
        players = [Turn, MC]
        files = ["final_states/HybridTurn.txt", "final_states/MonteCarlo.txt"]
        await getResults(players, files)

        players.clear()
        players = [Turn, Q]
        files = ["final_states/HybridTurn.txt", "final_states/QLite.txt"]
        await getResults(players, files)

        players.clear()
        players = [HP, MD]
        files = ["final_states/HybridHP.txt", "final_states/MaxDamPlan.txt"]
        await getResults(players, files)
        
        players.clear()
        players = [HP, MC]
        files = ["final_states/HybridHP.txt", "final_states/MonteCarlo.txt"]
        await getResults(players, files)

        players.clear()
        players = [HP, Q]
        files = ["final_states/HybridHP.txt", "final_states/QLite.txt"]
        await getResults(players, files)
        
        players.clear()
        players = [Info, MD]
        files = ["final_states/HybridInfo.txt", "final_states/MaxDamPlan.txt"]
        await getResults(players, files)
        
        players.clear()
        players = [Info, MC]
        files = ["final_states/HybridInfo.txt", "final_states/MonteCarlo.txt"]
        await getResults(players, files)

        players.clear()
        players = [Info, Q]
        files = ["final_states/HybridInfo.txt", "final_states/QLite.txt"]
        await getResults(players, files)
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())