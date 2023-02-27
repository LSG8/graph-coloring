# -*- coding: utf-8 -*-
"""
Created on Thur Feb 23 17:10:18 2023

@author: Lahari
"""
import sys
import random
from collections import deque

def valid_color(color, v_colors, adj_vertices):
    for i in adj_vertices:
        if v_colors[i] == color:
            return False
    return True

def assign_color(vertices, number_of_color, adj_list):
    v_colors = [-1]*len(vertices)
    color_list = [*range(number_of_color)]
    for i in vertices:
        for j in color_list:
            if valid_color(j, v_colors, adj_list[i]):
                v_colors[i] = j
                break
    return v_colors

def find_invalid_node(solution, adj_list):
    count = 0
    for idx, c in enumerate(solution):
        if not valid_color(c, solution, adj_list[idx]):
            count += 1
    return count

def valid_tabu_aspiration(test_tuple, tabu, temp_neighbor_invalid, best_invalid):
    if(len(tabu)>0):
        if test_tuple in tabu:
            if temp_neighbor_invalid < best_invalid: #check aspiration criteria
                tabu.remove(test_tuple)
                return True
            else:
                return False
    return True

def find_best_neighbor(neighbors,tabu_solution,tabu,adj_list,number_of_color):
    tabu_best = tabu_solution[:]
    tabu_tuple = None
    best_neighbor_invalid = len(tabu_solution) #start with the max value
    best_invalid = find_invalid_node(tabu_solution, adj_list)
    for _ in range(neighbors):
        change_v = random.randint(0,V-1)
        new_color = random.randint(0,(number_of_color-1))
        if tabu_solution[change_v] == new_color:
            new_color = number_of_color-1
        temp_neighbor = tabu_solution[:]
        temp_neighbor[change_v] = new_color
        temp_neighbor_invalid = find_invalid_node(temp_neighbor, adj_list)
        if valid_tabu_aspiration((change_v,new_color), tabu, temp_neighbor_invalid, best_invalid) and temp_neighbor_invalid < best_neighbor_invalid:
            tabu_best = temp_neighbor[:] #best neighbor
            tabu_tuple = (change_v,new_color)
            best_neighbor_invalid = find_invalid_node(tabu_best, adj_list)
        if temp_neighbor_invalid < best_invalid: #improvement found
            break
    return tabu_best, tabu_tuple

def tabu_search(tabu_iteration, tabu_size, neighbors, current_solution, number_of_color, adj_list):
    tabu = deque()
    tabu_solution = [(number_of_color-1) if x==-1 else x for x in current_solution]
    best = tabu_solution[:]
    best_invalid = find_invalid_node(best, adj_list)
    print("Start tabu search with {} colors ".format(number_of_color))
    #print(tabu_solution)
    for _ in range(tabu_iteration):
        best_neighbor, tabu_tuple = find_best_neighbor(neighbors,tabu_solution,tabu,adj_list,number_of_color)
        if tabu_tuple:
            tabu.append(tabu_tuple)
        if len(tabu) > tabu_size:
            tabu.popleft()
        neighbor_invalid = find_invalid_node(best_neighbor, adj_list)
        if neighbor_invalid == 0:#found coloring
            best = best_neighbor[:]
            break
        elif neighbor_invalid < best_invalid: #check if better neighborhood solution found
            best = best_neighbor[:]
            best_invalid = neighbor_invalid
        tabu_solution = best_neighbor[:] #continue neighborhood search with current solution (current solution may be better or not, means might take worse solution)
    return best

def read_input(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f]
    first_line = lines[0].split()
    V = int(first_line[0])
    E = int(first_line[1])
    adj_list = [[] for i in range(V)]
    for line in lines[1:]:
        edge = line.split()
        adj_list[int(edge[0])].append(int(edge[1]))
        adj_list[int(edge[1])].append(int(edge[0]))
    #print(adj_list)  
    return V, adj_list

# Driver Code
if __name__ == '__main__':
    try: #argument 1 :: input file
        input_file = sys.argv[1]
        V, adj_list = read_input(input_file) #access the graph as an adjacency list
    except:
        print("Please provide the input file as an argument")
    try: #optional argument 2 :: iteration value for tabu search
        tabu_iteration = sys.argv[2]
    except:
        print("No value in the second argument, working with the default tabu iteration (=10000)")
        tabu_iteration = 10000
    tabu_size = 0.2 * V  #tabu size = 20% of the problem size
    neighbor_size = 50  # number of random neighbors
    max_color = len(max(adj_list, key=len)) + 1 #upper bound of color = max degree of the graph
    vertices = [*range(V)]

    while max_color>2:
        do_tabu = True
        max_color-=1 #reduce the color value

        #find randomized greedy solution for current color value
        for i in range(100):
            random.shuffle(vertices) #random ordering of vertices
            new_solution = assign_color(vertices, max_color, adj_list) 
            if (-1 not in new_solution):
                best_solution = new_solution[:] #randomized greedy solution found coloring
                do_tabu = False #tabu search is not needed for this color value

        if do_tabu:
            #randomized greedy couldn't find a solution for current color value; try tabu search
            initial_solution = assign_color(vertices, max_color, adj_list) #generate a greedy solution
            random.shuffle(initial_solution) #shuffle the initial solution to make it random before tabu search
            current_best = max(best_solution) + 1
            print()
            print("Current best result = {} colors".format(current_best))
            tabu_best = tabu_search(tabu_iteration, tabu_size, neighbor_size, initial_solution, max_color, adj_list)
            if (find_invalid_node(tabu_best, adj_list) == 0): #tabu search found coloring for current color value
                best_solution = tabu_best[:]
                print("Found valid coloring")
            else: #tabu search couldn't find coloring for current color value
                print("Not found valid coloring")
                break  #no need to try with lesser color values
    print()
    print("****************************************************************")
    print("Final result")
    print("****************************************************************")
    print(max(best_solution) + 1)
    print(best_solution)