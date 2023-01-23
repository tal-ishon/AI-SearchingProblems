"""
Tal Ishon

"""
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main import find_idastar_route
from ways import load_map_from_csv, draw


# For Question 9 - graph plot of 100 problems
def get_data():
    x = pd.read_csv("resultsToGraph/Heuristic_cost.csv", names=['Heuristic_cost'])
    y = pd.read_csv("resultsToGraph/Real_cost.csv", names=['Real_cost'])
    return pd.concat([x, y], axis=1)  # merge 2 dfs into one


def create_graph(data):
    sns.set_theme(style="white", font_scale=1.5)
    # Set the font to Times new roman
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    # graph in and out
    plt.subplots(1, figsize=(8, 6))
    ax = sns.scatterplot(data=data, x='Heuristic_cost', y='Real_cost', s=80, color="green")
    ax.set_xlabel("Heuristic cost", fontsize=15)
    ax.set_ylabel("Real cost", fontsize=15)
    ax.set_title("A* Graph", fontsize=30)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()


# For Question 12 - draw 10 maps for 10 solutions
def create_map_drawing():
    roads = load_map_from_csv()
    with open('10_problems.csv') as problems_file:
        reader = csv.reader(problems_file)
        problems = []

        for row in reader:
            problems.append((int(row[0]), int(row[1])))

        for index, problem in enumerate(problems):
            source, target = problem
            path = find_idastar_route(int(source), int(target))
            name = "myPlot_" + str(index)
            draw.plot_path(roads, path, name)
            plt.show()

if __name__ == '__main__':
    # create graph for question 9
    create_graph(get_data())

    # create maps for question 12
    #create_map_drawing()