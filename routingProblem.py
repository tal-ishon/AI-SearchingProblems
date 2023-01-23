"""

Tal Ishon

"""
from functools import total_ordering
from utilityFunctions import PriorityQueue, huristic_function
from ways.info import SPEED_RANGES

# GLOBALS:
new_limit = float("inf")
h = huristic_function

def g(node):
    return node.path_cost


class RoutingProblem:
    def __init__(self, s_start, goal, G):
        self.s_start = s_start  # initiate the nodes in problem to be junctions
        self.goal = goal
        self.G = G
        self.junc_list = G.junctions()

    def is_goal(self, s):
        return s == self.goal

    def step_cost(self, a):
        # divide by 1000 cause distance in meters and speed in km per min
        return (a.distance / 1000) / max(SPEED_RANGES[a.highway_type])

    def state_str(self, s):
        return s

    def __repr__(self):
        return {'s_start': self.s_start, 'goal': self.goal, 'graph': self.G}


"""Definition of Node in a search graph"""


@total_ordering
class Node:
    def __init__(self, state, parent=None, path_cost=0):  # state means what node I am
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        nodes = []
        # return all links' numbers which are children of node (=junction)
        for link in problem.G[self.state].links:
            # generate new children nodes according to links in junction
            nodes.append(self.child_node(problem, link.target, link))

        return nodes  # returns all nodes' children

    def child_node(self, problem, next_state, link):
        next_node = Node(next_state, self,
                         self.path_cost + problem.step_cost(link))
        return next_node

    def solution(self):
        return [node.state for node in self.path()[:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return f"<{self.state}>"

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.state)


def best_first_graph_search(problem, Astar, f, h):
    node = Node(problem.s_start)
    frontier = PriorityQueue(f)  # Priority Queue
    frontier.append(node)
    closed_list = set()
    p_junction = problem.junc_list  # todo: check if it works if not bring it back to origin (lines 97-98, 90-91)
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state) and not Astar:
            return node.solution(), node.path_cost
        elif problem.is_goal(node.state) and Astar:  # return also huristic cost
            # todo: check if function need to return cost or just path
            return node.solution(), node.path_cost, \
                   h(p_junction[problem.goal].lat, p_junction[problem.goal].lon,
                     p_junction[problem.s_start].lat, p_junction[problem.s_start].lon)
        closed_list.add(node.state)  # add node that we visited in order to avoid loops
        for child in node.expand(problem):  # expanding all node's children
            if child.state not in closed_list and child not in frontier:  # add to frontier only nodes we haven't visited yet
                frontier.append(child)
            elif Astar and child in frontier \
                    and f(child) + h(p_junction[problem.goal].lat, p_junction[problem.goal].lon,
                                     p_junction[child.state].lat, p_junction[child.state].lon) < frontier[child]:
                del frontier[child]  # from before and add node to frontier
                frontier.append(child)
            elif not Astar and child in frontier and \
                    f(child) < frontier[child]:  # if there is a cheaper path delete the node
                del frontier[child]  # from before and add node to frontier
                frontier.append(child)

    return None, None  # if there is no path


def ida_cost_search(problem):
    global new_limit

    start_junction = problem.G[problem.s_start]
    final_junction = problem.G[problem.goal]

    new_limit = h(start_junction.lat, start_junction.lon, final_junction.lat, final_junction.lon)

    while True:
        f_limit = new_limit
        new_limit = float("inf")
        solution = DFS_f(Node(problem.s_start), f_limit, Node(problem.goal), problem)
        if solution is not None:
            return solution


def DFS_f(node, f_limit, goal_node, problem):
    # calculate heuristic distance
    h_cost = h(problem.G[node.state].lat, problem.G[node.state].lon,
               problem.G[goal_node.state].lat, problem.G[goal_node.state].lon)

    # create a new limit
    new_f = g(node) + h_cost

    # check if new limit is higher than current limit
    if new_f > f_limit:
        global new_limit
        new_limit = min(new_limit, new_f)
        return None
    if goal_node.state == node.state:
        return node.solution()
    for c in node.expand(problem):
        solution = DFS_f(c, f_limit, goal_node, problem)
        if solution is not None:
            return solution
    return None


# f = g:
def uniform_cost_search(problem, Astar):
    if Astar:
        return best_first_graph_search(problem, Astar, g, huristic_function)
    else:
        return best_first_graph_search(problem, Astar, g, False)


# to write all info into results file-
def write_ucs_info_path(source, target, G):
    return uniform_cost_search(RoutingProblem(source, target, G), False)



# to write all info into results file-
def write_astar_info_path(source, target, G):
    return uniform_cost_search(RoutingProblem(source, target, G), True)



# to create 10 problems and make maps out of them (question 12)
def write_idastar_info_path(source, target, G):
    return ida_cost_search(RoutingProblem(source, target, G))





