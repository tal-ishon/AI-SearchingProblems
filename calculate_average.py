"""
Tal Ishon


"""
import csv
from main import find_idastar_route, find_astar_route, find_ucs_route
import time

def run_time_average():
    with open('10_problems.csv') as problems_file:
        reader = csv.reader(problems_file)
        problems = []

        for row in reader:
            problems.append((int(row[0]), int(row[1])))

        usc_times = []
        astar_times = []
        idastar_times = []

        for problem in problems:
            source, target = problem
            source = int(source)
            target = int(target)

            # usc:
            t0 = time.time()
            find_ucs_route(source, target)
            tn = time.time()
            usc_times.append(tn - t0)

            # astar:
            t0 = time.time()
            find_astar_route(source, target)
            tn = time.time()
            astar_times.append(tn - t0)

            # idastar:
            t0 = time.time()
            find_idastar_route(source, target)
            tn = time.time()
            idastar_times.append(tn - t0)

        if len(usc_times) != 0:
            print("UCS average run time: ", sum(usc_times) / len(usc_times))
        if len(astar_times) != 0:
            print("AStar average run time: ", sum(astar_times) / len(astar_times))
        if len(idastar_times) != 0:
            print("IDAStar average run time: ", sum(idastar_times) / len(idastar_times))


if __name__ == '__main__':
    run_time_average()