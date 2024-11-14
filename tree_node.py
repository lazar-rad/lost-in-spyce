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

def default_heuristics(state):
    return 0

def coords(n):
    b = int(math.log2(n))
    return (int(b / config.N), b % config.N)

def dist(c1, c2):
    return int(abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]))

def manhattan(state):
    goals_list = []
    goals = state.goals
    while goals:
        goals_list.append(coords(goals & -goals))
        goals &= goals - 1
    spaceships = state.spaceships
    h = 0
    while spaceships:
        s = coords(spaceships & -spaceships)
        h_part = config.M + config.N
        for goal in goals_list:
            d = dist(s, goal)
            h_part = d if d < h_part else h_part
        h += h_part
        spaceships &= spaceships - 1
    return h

class TreeNode:
    expanded_nodes = 0
    lex_sort = lambda ch: ch.map_node.name
    dist_sort = lambda ch: ch.parent.map_node.distance_to(ch.map_node)
    children_sort_key = lex_sort
    heuristics = default_heuristics

    @staticmethod
    def set_heuristics(heur=default_heuristics):
        TreeNode.heuristics = heur

    def __init__(self, action, state):
        self.action = action
        self.state = state
        self.children = []
        self.parent = None
        self.expansion_order = 0
    
    def add_child(self, tree_node):
        if (not tree_node.parent) and not (tree_node in self.children):
            self.children.append(tree_node)
            tree_node.parent = self

    def get_path(self):
        if self.parent:
            return self.parent.get_path() + [self.action]
        else:
            return []

    def get_path_cost(self):
        if self.parent:
            return self.parent.get_path_cost() + State.get_action_cost(self.action)
        else:
            return 0

    def get_path_length(self):
        if self.parent:
            return self.parent.get_path_length() + 1
        else:
            return 0
    
    def get_path_as_string(self):
        if self.parent:
            return self.parent.get_path_as_string() + " -> " + f"({self.expansion_order})"
        else:
            return f"({self.expansion_order})"

    def visited(self, state):
        if self.state == state:
            return True
        if not self.parent:
            return False
        return self.parent.visited(state)

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
        exp_ord = self.expansion_order if self.expansion_order > 0 else '_'
        act = action_repr(self.action)
        stt = f"{self.state.get_state(Spaceship.kind()):x}".zfill((config.M * config.N + 3)//4)
        return f"({exp_ord}): {act} => {stt}"

    def construct_suffix(self, template=""):
        if len(template) == 0:
            return ""
        template = template.replace('$c', f"{self.get_path_cost()}")
        template = template.replace('$l', f"{self.get_path_length()}")
        template = template.replace('$h', f"{TreeNode.heuristics(self.state)}")
        return ' ' + template

    def to_string(self, suffix_template="", prefix=""):
        s = prefix + str(self) + self.construct_suffix(suffix_template) +  '\n'
        if len(self.children) > 0:
            prefix = extend_down(prefix)
            for ch in self.children[:-1]:
                s += ch.to_string(suffix_template, prefix + box_vert_right + box_hor)
            s += self.children[-1].to_string(suffix_template, prefix + box_up_right + box_hor)
        return s