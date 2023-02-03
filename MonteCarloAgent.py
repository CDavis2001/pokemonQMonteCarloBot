from poke_env.player import Player
from MonteCarloNode import Node
from poke_env.environment import Pokemon
from utility import embed_battle

class MonteCarloPlayer(Player):
    def choose_move(self, battle):
        self.plan = []
        
        state = embed_battle(battle)
        
        # check if plan exists
        if len(self.plan) > 0:
            # get first action in plan
            action = self.plan[0]
            self.plan.pop(0)
            # if the expected state in the plan matches the actual state,
            # follow the plan
            if action[0] == state:
                if action[1][0] == "use":
                    return self.create_order(action[1][1])
                else:
                    return self.create_order(Pokemon(species=action[1][1]))
            # otherwise clear the plan
            else:
                print("replanning")
                self.plan = []
                
        self.tree = []
        # build tree
        root = Node(None,state,None)
        queue = [root]
        endstates = 0
        while len(queue) > 0 and endstates < 10:
            node = queue.pop(0)
            self.tree.append(node)
            for action in node.untried_actions:
                children = node.simulate(action)
                for child in children:
                    node.children.append(child)
            
                    if child.is_end_state() != 0:
                        endstates += 1
                        child.back_propagate(child.is_end_state())
                    else:
                        
                        queue.append(child)
                
        self.tree.extend(queue)
        # end build tree
        
        
        # make plan
        self.plan = []
        node = self.tree[0]
        while node.is_end_state() == 0:
            max_wl_diff = -2000000000
            step = []
            successor = None
            if len(node.children) == 0:
                
                break
            for child in node.children:
                
                wl_diff = child.results[1] - child.results[-1]
                if wl_diff > max_wl_diff:
                    
                    max_wl_diff = wl_diff
                    step = [node.state, child.action]
                    successor = child
            
            self.plan.append(step)
            node = successor
        
        # and make plan
        
        
        
        if len(self.plan) == 0:
            print("made plan, empty")
            return(self.choose_random_move(battle))
        action = self.plan[0]
        self.plan.pop(0)
        print(len(action))
        if action[1][0] == "use":
            return self.create_order(action[1][1])
        else:
            return self.create_order(Pokemon(species=action[1][1]))
        
    
    
    
    
    
    
    
    
    
    
    # node, action -> node
    def simulate():
        return
    
    