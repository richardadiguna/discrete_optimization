import re
import os
import math


class DynamicProgramming:
    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.opt_value = 0
        self.opt_taken = [0]*len(items)

    def resolve(self):
        min_weight = min([item.weight for item in self.items])
        dynamic_table = []

        for i in range(len(self.items)+1):
            column = []
            item_value, item_weight = self.items[i-1].value, self.items[i-1].weight

            for j in range(self.capacity+1):
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
            if dynamic_table[i][self.capacity-weight] > dynamic_table[i-1][self.capacity-weight]:
                if weight + self.items[i-1].weight <= self.capacity:
                    self.opt_taken[self.items[i-1].index] = 1
                    self.opt_value += self.items[i-1].value
                    weight += self.items[i-1].weight
        
        return self.opt_value, self.opt_taken
