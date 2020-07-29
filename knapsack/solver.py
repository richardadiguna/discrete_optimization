#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from dynamic_programming import DynamicProgramming
Item = namedtuple("Item", ['index', 'value', 'weight'])

# Greedy Algoirthm
# Dynamic Programming
# Depth First

def get_sort_preference(index):
    if index == 0:
        return lambda x: x.value
    if index == 1:
        return lambda x: x.weight
    if index == 2:
        return lambda x: x.value / x.weight


def solve_it(input_data, method='DP'):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    
    opt_value = 0
    opt_taken = [0]*len(items)

    # sort items by value density
    if method == 'GR':
        for i in range(3):
            value = 0
            weight = 0
            taken = [0]*len(items)
            sortby = get_sort_preference(i)
            sorted_items = sorted(items, key=sortby, reverse=True)

            for item in sorted_items:
                if weight + item.weight <= capacity:
                    taken[item.index] = 1
                    value += item.value
                    weight += item.weight

            if opt_value < value:
                opt_value = value
                opt_taken = taken
    
    if method == 'DP':
        solver = DynamicProgramming(capacity, items)
        opt_value, opt_taken = solver.resolve()
        min_weight = min([item.weight for item in items])
        dynamic_table = []

        for i in range(len(items)+1):
            column = []
            item_value, item_weight = items[i-1].value, items[i-1].weight

            for j in range(capacity+1):
                if i == 0 or j == 0:
                    column.append(0)
                else:
                    if item_weight <= j:
                        optimal_1 = dynamic_table[i-1][j] # O(K, J-1)
                        optimal_2 = item_value + dynamic_table[i-1][j-item_weight] # Vj + O(K-Wj, J-1)

                        optimal_solution = max(optimal_1, optimal_2)
                        column.append(optimal_solution)
                    else:
                        optimal_solution = dynamic_table[i-1][j]
                        column.append(optimal_solution)
                        
            dynamic_table.append(column)

        weight = 0

        for i in range(len(dynamic_table)-1, 0, -1):
            if dynamic_table[i][capacity-weight] > dynamic_table[i-1][capacity-weight]:
                if weight + items[i-1].weight <= capacity:
                    opt_taken[items[i-1].index] = 1
                    opt_value += items[i-1].value
                    weight += items[i-1].weight

    if method == 'BB':
        # given a set X {xi: item on ith index} e.g. x1, x2, x3
        # take the item or don't take the item
        # iterate the same process until the last item
        
        # find an optimistic estimate of the best solution to the subproblem (bounding)
        # (1) take the problem and relax it 
        # relax capacity constraint
        # there are 3 entries (value, capacity, estimate)
        # if we decide to not to take the item estimate value will be decrease by the value of that item
        # if the capacity reduce to below zero we can't take the item

        # - store the best current solution and compare to estimate value on another branch
        # - setup a logic where you don't have to explore anymore below the tree 
        #   if the estimate value is worse than the best solution
        # - relaxation should be integer after dividing value and weight 
        # order the items by value/kilos
        # select the most valuable items until the capacity is exhausted the select a fraction of 
        # next item and fill the knapsack
        # (Wi/Vi)*Yi <= K where 

        # use depth first / least discrepancy
        # best first search choose the best estimation value on the children node
        # limited discrepancy search 

        # relaxation code here
        items = sorted(items, key=lambda x: x.value/x.weight, reverse=True)
        weight = 0
        estimation = 0
        for item in items:
            if weight + item.weight <= capacity:
                weight += item.weight
                estimation += item.value
            else:
                residual_weight = capacity - weight
                partition_weight = residual_weight / item.weight 
                partition_value = round(partition_weight * item.value)
                weight += residual_weight
                estimation += partition_value
        
        print(estimation)

        # depth first search code here
        visited = [[False]*2]*len(items)
        print(visited)

        def recursion(capcity, ):
            value = None
            return value

        for i, branch in enumerate(visited):
            for j, state in enumerate(branch):
                # if visited[i][j] == False:
                print(i, j)

        from collections import defaultdict 

        graph = defaultdict(list) 
        graph[0].append(1)
        graph[0].append(2)
        graph[1].append(5)
        graph[1].append(8)
        graph[2].append(10)
        graph[2].append(9)

        print(graph)
        print(max(graph)+1)
        print(graph[0])

    # prepare the solution in the specified output format
    output_data = str(opt_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, opt_taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

