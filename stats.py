"""
Tal Ishon

"""

from collections import namedtuple, Counter
from ways import load_map_from_csv, Roads


def map_statistics(roads: Roads):
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    'get number of junctions'
    num_of_junctions = len(roads)
    outgoing_branching_factor_list = []
    distance_list = []
    road_type_list = []
    'go over all junctions'
    for junction in roads.values():
        'get list of numbers of branches'
        outgoing_branching_factor_list.append(len(junction.links))
        for link in junction.links:
            distance_list.append(link.distance)
            road_type_list.append(link.highway_type)
    num_of_links = sum(outgoing_branching_factor_list)
    max_outgoing_branch = max(outgoing_branching_factor_list)
    min_outgoing_branch = min(outgoing_branching_factor_list)
    avr_outgoing_branch = num_of_links / num_of_junctions
    sum_distances = sum(distance_list)
    max_distance = max(distance_list)
    min_distance = min(distance_list)
    avr_distance = sum_distances / num_of_links
    print(list(roads.iterlinks()))
    return {
        'Number of junctions': num_of_junctions,
        'Number of links': num_of_links,
        'Outgoing branching factor': Stat(max=max_outgoing_branch, min=min_outgoing_branch, avg=avr_outgoing_branch),
        'Link distance': Stat(max=max_distance, min=min_distance, avg=avr_distance),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram': Counter(road_type_list)
    }


def print_stats():
    roads = load_map_from_csv()
    for k, v in map_statistics(roads).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
