import random
import os
from datetime import datetime

from tree_node import *

class Algorithm:
    def __init__(self):
        self.nodes_to_expand = []
        self.root = None
        self.start = None
        self.final = None
        self.check_at_gen = False
        self.suffix_template = ""
        self.msg = None

    def get_path(self, state):
        self.nodes_to_expand = []
        self.start = state
        self.root = TreeNode(None, self.start)
        self.nodes_to_expand.append(self.root)
        self.final = self.root if self.root.state.is_goal_state() else None
        while not self.final and len(self.nodes_to_expand) > 0:
            self.final = self.search_step()
            if self.final:
                self.log_search()
                return self.final.get_path()
        print("Path not found")
        return []
    
    def search_step(self):
        tree_node = self.nodes_to_expand.pop(0)
        if tree_node.state.is_goal_state():
            tree_node.check_as_expanded()
            return tree_node
        if self.worth_expanding(tree_node):
            ret_node = tree_node.expand(self.check_at_gen)
            if ret_node:
                ret_node.check_as_expanded()
            self.update_nodes_to_expand(tree_node)
            return ret_node
        return None

    def update_nodes_to_expand(self, exp_tree_node):
        pass
    
    def worth_expanding(self, tree_node):
        return True
    
    def log_search(self):
        search_log = open(os.path.join(config.LOG_FOLDER, f'SEARCH_LOG_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.txt'), 'w')
        search_log.write(self.msg + '\n')
        search_log.write('\n')
        search_log.write("nodes: " + self.final.get_path_as_string() + '\n')
        search_log.write("actions: " + str(self.final.get_path()) + '\n')
        search_log.write('\n')
        search_log.write(self.root.to_string(self.suffix_template))
        search_log.close()



class ExampleAlgorithm(Algorithm):
    def get_path(self, state):
        path = []
        while not state.is_goal_state():
            possible_actions = state.get_legal_actions()
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
            path.append(action)
            state = state.generate_successor_state(action)
        return path


class Blue(Algorithm):
    def __init__(self):
        super().__init__()
        self.msg = "I am Blue and I use DFS!"

    def update_nodes_to_expand(self, exp_tree_node):
        self.nodes_to_expand = exp_tree_node.children + self.nodes_to_expand


class Red(Algorithm):
    def __init__(self):
        super().__init__()
        self.check_at_gen = True
        self.msg = "I am Red and I use BFS!"

    def update_nodes_to_expand(self, exp_tree_node):
        self.nodes_to_expand += exp_tree_node.children

        
class Black(Algorithm):
    def __init__(self):
        super().__init__()
        self.suffix_template = "[$c]"
        self.msg = "I am Black and I use Branch-and-bound!"

    def update_nodes_to_expand(self, exp_tree_node):
        self.nodes_to_expand += exp_tree_node.children
        self.nodes_to_expand.sort(key = lambda node: (node.get_path_cost(), node.action[0], action_direction(node.action)))

        
class White(Algorithm):
    def __init__(self):
        super().__init__()
        self.suffix_template = "[$c+$h]"
        self.msg = "I am White and I use A* with Manhattan heuristics!"
        TreeNode.set_heuristics(manhattan)

    def update_nodes_to_expand(self, exp_tree_node):
        self.nodes_to_expand += exp_tree_node.children
        self.nodes_to_expand.sort(key = lambda node: (node.get_path_cost() + TreeNode.heuristics(node.state), node.action[0], action_direction(node.action)))

#    def get_path(self, state):
#        print("*** Testing heuristics ***")
#        print(TreeNode.heuristics(state))
#        print("**************************")
#        exit()