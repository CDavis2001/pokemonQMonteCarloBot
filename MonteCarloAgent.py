from poke_env.player import Player
from QLearningAgent import embed_battle
from MonteCarloNode import Node

class MonteCarloPlayer(Player):
    def __init__(self, team):
        self.plan = []
        self.team = team
        self.tree
        return
    
    def choose_move(self, battle):
        state = embed_battle(battle)
        # check if plan exists
        if len(self.plan) > 0:
            # get first action in plan
            action = self.plan[0]
            self.plan.pop(0)
            # if the expected state in the plan matches the actual state,
            # follow the plan
            if action[0] == state:
                return action
            # otherwise clear the plan
            else:
                self.plan = []
                
        
        # make a plan
        root = Node(None,state,None)
        stack = [root]
        self.build_tree(battle, stack)
        self.tree = root
        self.plan = self.make_plan(root,battle)
        
    
    def build_tree(self, battle, stack):
        if len(stack) == 0:
            return
        
        state = stack.pop(-1)
        for action in state.untried_actions:
            child = state.simulate(action)
            state.children.append(child)
            
            if child.is_end_state() != 0:
                self.back_propagate(child.is_end_state())
            else:
                stack.append(child)
                
        return self.build_tree(battle, stack)
    
    
    def make_plan(self, state, plan):
        max_wl_ratio = 0
        step = [None, None]
        successor = None
        if len(state.children) == 0:
            return
        for child in state.children:
            wl_ratio = child.results[1] / child.results[-1]
            if wl_ratio > max_wl_ratio:
                max_wl_ratio = wl_ratio
                step[0] = state.state
                step[1] = state.action
                successor = child
                
        plan.append(step)
        return self.make_plan(state, successor, plan)
    
    # node -> node
    def selection(node):
        return
    
    # node -> node
    def expansion():
        return
    
    # node -> float
    def simulation():
        return
    
    # [node], float
    def backpropagation():
        return