import math

import config
from sprites import Spaceship
from state import State

box_hor = '─'
box_vert = '│'
box_vert_right = '├'
box_up_right = '└'
box_empty = ' '

def extend_down(si):
    so = ""
    for c in si:
        if c in [box_hor, box_up_right, box_empty]:
            so += box_empty
        elif c in [box_vert, box_vert_right]:
            so += box_vert
        else:
            so += box_empty
    return so

def action_repr(act):
    if act == None:
        return "noAction"
    else:
        return f"({act[0][0]},{act[0][1]})->({act[1][0]},{act[1][1]})"

def action_direction(act):
    if act == None:
        return 4
    elif act[1][0] < act[0][0]:
        return 0
    elif act[1][1] > act[0][1]:
        return 1
    elif act[1][0] > act[0][0]:
        return 2
    elif act[1][1] < act[0][1]:
        return 3
    else:
        return 4



class TreeNode:
    expanded_nodes = 0

    def __init__(self, action, state):
        self.action = action
        self.state = state
        self.children = []
        self.parent = None
        self.expansion_order = 0
        self.path_cost = 0
        self.depth = 0
        self.sorting_tuple = None
        self.heuristics = 0
    
    def add_child(self, tree_node):
        if (not tree_node.parent) and not (tree_node in self.children):
            self.children.append(tree_node)
            tree_node.parent = self
            tree_node.path_cost = tree_node.parent.path_cost + State.get_action_cost(tree_node.action)
            tree_node.depth = tree_node.parent.depth + 1

    def get_path(self):
        path = []
        tree_node = self
        while tree_node.parent:
            path = [tree_node.action] + path
            tree_node = tree_node.parent
        return path

    def get_path_as_string(self):
        path_str = f"({self.expansion_order})"
        tree_node = self
        while tree_node.parent:
            path_str = f"({tree_node.parent.expansion_order})" + " -> " + path_str
            tree_node = tree_node.parent
        return path_str

    def visited(self, state):
        tree_node = self
        while tree_node:
            if tree_node.state == state:
                return True
            tree_node = tree_node.parent
        return False

    def expand(self, check_at_gen=False):
        if self.expansion_order == 0:
            TreeNode.expanded_nodes += 1
            self.expansion_order = TreeNode.expanded_nodes
            print(f"Node expanded: action = {self.action}, order = {self.expansion_order}")
            for action in self.state.get_legal_actions():
                successor = self.state.generate_successor_state(action)
                if not self.visited(successor):
                    tree_node = TreeNode(action, successor)
                    self.add_child(tree_node)
                    if check_at_gen and successor.is_goal_state():
                        return tree_node
        else:
            print("Node already expanded")   
        return None

    def check_as_expanded(self):
        if self.expansion_order == 0:
            TreeNode.expanded_nodes += 1
            self.expansion_order = TreeNode.expanded_nodes
        return None

    def __str__(self):
        exp_ord = self.expansion_order
        if self.expansion_order == 0:
            exp_ord = '_'
        elif self.expansion_order == -1:
            exp_ord = 'x'
        act = action_repr(self.action)
        stt = f"{self.state.get_state(Spaceship.kind()):x}".zfill((config.M * config.N + 3)//4)
        return f"({exp_ord}): {act} => {stt}"

    def construct_suffix(self, template=""):
        if len(template) == 0:
            return ""
        template = template.replace('$c', f"{self.path_cost}")
        template = template.replace('$l', f"{self.depth}")
        template = template.replace('$h', f"{self.heuristics}")
        return ' ' + template

    def to_string(self, suffix_template="", prefix=""):
        s = prefix + str(self) + self.construct_suffix(suffix_template) +  '\n'
        if len(self.children) > 0:
            prefix = extend_down(prefix)
            for ch in self.children[:-1]:
                s += ch.to_string(suffix_template, prefix + box_vert_right + box_hor)
            s += self.children[-1].to_string(suffix_template, prefix + box_up_right + box_hor)
        return s