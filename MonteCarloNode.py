class Node:
    def __init__(self, parent, state, action):
        self.parent = parent
        self.state = state
        self.action = action
        self.children = []
        self.endstate = False
        self.num_visits = 0
        self.results[1] = 0
        self.results[-1] = 0
        self.untried_actions = None
        return
    
    def is_end_state(self):
        result = 0
        if self.state["observation"]["active_pokemon"]["hp"] == 0:
            loss = True
            for pkmn in self.state["observation"]["team"]:
                if pkmn["hp"] != 0:
                    loss == False
                    
        if loss:
            result = -1
        
        if len(self.state["observation"]["opponent_team"]) == 6:
            total_hp = 0
            for pkmn in self.state["observation"]["opponent_team"]:
                total_hp += pkmn["hp"]
            if total_hp == 0:
                result = 1
        return result