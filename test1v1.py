from poke_env.player.player import Player
from poke_env.data import to_id_str
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from concurrent.futures import Future
import asyncio

async def onev1_evaluate(
    players: List[Player], n_challenges: int
):
    # player 1 issues challenge to player 2 and player 2 accepts to begin battle
    for i, p_1 in enumerate(players):
        for j, p_2 in enumerate(players):
            if j <= i:
                continue
            await asyncio.gather(
                p_1.send_challenges(
                    opponent=to_id_str(p_2.username),
                    n_challenges=n_challenges,
                    to_wait=p_2.logged_in,
                ),
                p_2.accept_challenges(
                    opponent=to_id_str(p_1.username), n_challenges=n_challenges
                ),
            )
            # collect results to return
            results = dict()
            results[p_1.username] = [p_1.win_rate, n_challenges]
            results[p_2.username] = [p_2.win_rate, n_challenges]
            
            

            # reset players
            p_1.reset_battles()
            p_2.reset_battles()
    return results  