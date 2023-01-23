"""
Tal Ishon

"""
from routingProblem import uniform_cost_search, RoutingProblem, ida_cost_search
from ways.graph import load_map_from_csv

G = load_map_from_csv()

def find_ucs_route(source, target):
    # return the fastest route
    return uniform_cost_search(RoutingProblem(source, target, G), False)[0]


def find_astar_route(source, target):
    # return the fastest route
    return uniform_cost_search(RoutingProblem(source, target, G), True)[0]


def find_idastar_route(source, target):
    # return the fastest route
    return ida_cost_search(RoutingProblem(source, target, G))[0]
    

def dispatch(argv):
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_route(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)

