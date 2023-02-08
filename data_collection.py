import asyncio
from MaxDamageAgent import MaxDamagePlayer
from MaxDamagePlanAgent import MaxDamagePlanPlayer
from QLearningAgent import QLearningPlayer
from MonteCarloAgent import MonteCarloPlayer
from tabulate import tabulate
from poke_env.player import cross_evaluate, RandomPlayer
from QLearningAgentLite import QLearningLitePlayer
from test1v1 import onev1_evaluate

async def main():
    file = open("Teams/SpecsLelePult noswitchmoves.txt")
    team = file.read()
    file.close()
    players = []
    #players.append(RandomPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(MaxDamagePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(MaxDamagePlanPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(QLearningPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    players.append(MonteCarloPlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    #players.append(QLearningLitePlayer(battle_format="gen8ou", team=team, start_timer_on_battle_start=True))
    
    for i in range(500):
        
        #cross_evaluation = await cross_evaluate(players,challenges)
        cross_evaluation = await onev1_evaluate(players, 1)
        file = open("results.txt", "a")
        
        states = []    
        states.append(open("final_states/MaxDamPlan.txt"))
        states.append(open("final_states/QLite.txt"))
        #states.append(open("final_states/MonteCarlo.txt"))
        
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




if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    