import asyncio
from MaxDamageAgent import MaxDamagePlayer
from MaxDamagePlanAgent import MaxDamagePlanPlayer
from QLearningAgent import QLearningPlayer
from MonteCarloAgent import MonteCarloPlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate, RandomPlayer
from QLearningAgentLite import QLearningLitePlayer
from test1v1 import onev1_evaluate
from HybridHPSwitch import HybridHPSwitchPlayer
from HybridInfoSwitch import HybridInfoSwitchPlayer
from HybridTurnSwitch import HybridTurnSwitchPlayer

async def main():
    
    # set number of battles
    iterations = 1000
    
    file = open("Teams/SpecsLelePult noswitchmoves.txt")
    team = file.read()
    file.close()
    players = []
    
    # Uncomment the agents that are desired for simulating and comment the others out
    
    #players.append(RandomPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(MaxDamagePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(MaxDamagePlanPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(QLearningPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(MonteCarloPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(QLearningLitePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(HybridTurnSwitchPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(HybridHPSwitchPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(HybridInfoSwitchPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(MonteCarloPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1))
    players.append(QLearningLitePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True, max_concurrent_battles=1))
    
    for i in range(iterations):
        
        
        cross_evaluation = await onev1_evaluate(players, 1)
        file = open("results/results.txt", "a")
        
        # uncomment the files corresponding to the desired agents and comment the others out
        
        states = []
        #states.append(open("final_states/MaxDamPlan.txt"))
        states.append(open("final_states/MonteCarlo.txt"))
        states.append(open("final_states/QLite.txt"))
        #states.append(open("final_states/MonteCarlo.txt"))
        #states.append(open("final_states/HybridHP.txt"))
        #states.append(open("final_states/HybridTurn.txt"))
        #states.append(open("final_states/HybridInfo.txt"))
        
        # read utility from files
        utility = []
        for state in states:
            utility.append(float(state.read()))
            state.close()
        
        
        # write results to file
    
        for key in cross_evaluation:
            if cross_evaluation[key][0] == 0:
                file.write("LOSS;" + key + ";" + str(max(utility)) + "\n")
            else:
                file.write("WIN;" + key + ";" + str(max(utility)) + "\n")
        file.close()




if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    