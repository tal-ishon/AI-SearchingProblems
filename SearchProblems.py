"""

Tal Ishon

"""
import csv
import random
import pandas as pd

from routingProblem import write_astar_info_path, write_idastar_info_path, write_ucs_info_path
from ways.graph import Roads, load_map_from_csv

G = load_map_from_csv()

def find_target(source, junctions):
    target = junctions[source.links[0].target]  # make sure before there is at least one link in links
    step_limit = random.randint(5, 10)  # limit steps length to be between 5 and 10
    counter = 0
    # making sure route has no loops
    while counter < step_limit or source.index == target.index:
        if len(target.links) == 0:  # in case target couldn't get to step_limit
            break
        target = junctions[target.links[0].target]
        counter += 1

    return source.index, target.index


def create_dictionary(rand_source_list, filtered, junctions):
    hundred_search_problems = {}
    for source in rand_source_list:
        real_source, target = find_target(filtered[source], junctions)
        hundred_search_problems[real_source] = target
    return hundred_search_problems


def random_search_problem(roads: Roads, num_problems, file_name):
    junctions = roads.junctions()

    # filter all junctions that are dead ends
    filtered = list(filter(lambda j: len(j.links) > 0, junctions))

    # generate a random source nodes list
    rand_source_list = random.sample(range(len(filtered)), num_problems)  # make sure all routes are unique

    # generate source: target dictionary
    hundred_search_problems = create_dictionary(rand_source_list, filtered, junctions)

    # convert dict to list
    problems_list = [(k, v) for k, v in hundred_search_problems.items()]

    # need to write the problems to a file
    problems = pd.DataFrame(problems_list)
    problems.to_csv(f'{file_name}.csv', encoding='utf-8', header=False, index=False)


def run_problem(algorithm, read_file, directory, file_name, type):  # func to run all 3 algorithm
    with open(f'{read_file}.csv', mode='r') as f:
        reader = csv.reader(f)
        string = ""
        for row in reader:
            temp_tuple = algorithm(int(row[0]), int(row[1]), G)

            if file_name == "UCSRuns":
                path, cost = temp_tuple
                path = ' '.join(str(s) for s in path)
                cost = round(cost, 4)  # make sure only 4 digits after dot
                string = path + ' - ' + str(cost) + '\n'

            elif file_name == "AStarRuns":
                path, cost, h_cost = temp_tuple
                path = ' '.join(str(s) for s in path)
                cost = round(cost, 4)  # make sure only 4 digits after dot
                h_cost = round(h_cost, 4)
                string = path + ' - ' + str(cost) + ' - ' + str(h_cost) + '\n'

            elif file_name == "IDAstarRuns":
                path = temp_tuple
                path = ' '.join(str(s) for s in path)
                string = path + "\n"

            with open(f'{directory}/{file_name}.{type}', 'a') as t:
                t.write(string)


# generate 100 problems (question 3)
def hundred_problems_question3():
    random_search_problem(G, 100, "problems")

# generate 10 problems (question 12)
def ten_problems_question12():
    random_search_problem(G, 10, "10_problems")

# use to get csv files only with costs (one file - real cost, second -heuristic cost) without path
# in order to create the graph (question 9)
def run_and_get_cost(algorithm, read_file, file_name):
    with open(f'{read_file}.csv', mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            cost = algorithm(int(row[0]), int(row[1]), G)[-1]
            cost = round(cost, 4)  # make sure only 4 digits after dot
            string = str(cost) + "\n"
            with open(f'{file_name}.csv', 'a') as t:
                t.write(string)

# in order to get only cost without path in "run_and_get_cost" function
# we put the right input
def write_UCS_cost_to_csv():
    run_and_get_cost(write_ucs_info_path, "results/UCSRuns", "resultsToGraph/Real_cost")

def write_Astar_cost_to_csv():
    run_and_get_cost(write_astar_info_path, "results/AStarRuns", "resultsToGraph/Heuristic_cost")


if __name__ == '__main__':

    # # Generate routing problems
    # hundred_problems_question3()
    #
    # # write problems for question 5:
    # run_problem(write_ucs_info_path, "problems", "results", "UCSRuns", "txt")
    #
    # # write problems for question 9:
    # run_problem(write_astar_info_path, "problems", "results", "AStarRuns", "txt")

    # read the problems file and generate from it help files which from whom we make the graph
    run_and_get_cost(write_ucs_info_path, "problems", "resultsToGraph/Real_cost")
    run_and_get_cost(write_astar_info_path, "problems", "resultsToGraph/Heuristic_cost")

    # # Generate routing problems
    # ten_problems_question12()
    #
    # # write 10 idastar routes into a csv file inorder to make the photos out of them (question 12)
    # run_problem(write_idastar_info_path, "10_problems", "resultsToGraph", "IDAstarRuns", "csv")



