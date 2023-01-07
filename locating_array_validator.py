import itertools
import math
import random
import time
import os
import operator 
import multiprocessing
from math import factorial
from itertools import combinations

start_time = time.time()
t = 2  #num of columns in interaction
v = 2  #num of values    
d = 1  #the size of the set of interactions
k = 4  #num of columns
n = 8 #starting num of rows
pop_size = 200 # population size

#Random Array Generation

#directory handeling


class individual_array:
    def __init__(self, array, fitness):
        self.array = array
        self.fitness = fitness

test = individual_array([[0,1],[1,0]],1)


if os.path.exists(os.getcwd()+f"/{k}_{n}"):
    path = os.getcwd()+f"/{k}_{n}"
else:
    os.mkdir(os.getcwd()+f"/{k}_{n}")
    path = os.getcwd()+f"/{k}_{n}"

set_of_interactions = set(itertools.product(itertools.combinations(range(k),t), itertools.product(range(v),repeat=t))) #generates set of interactions at t strength
dset = set(itertools.combinations(set_of_interactions, d)) #generates interactions of interacts of d strength


def set_iteration(input_array, dset):                                       # (((1, 3), (0, 1)),) {2} Outputs will look like this
    subset = set()                                                          # (1,3) < refers to the columns here
    for index, row in enumerate(input_array):                               # (0, 1) refers to the interaction occuring
        for cols, vals in dset:                                             # {2} refers to the index of the row in which teh output is found
            vals_in_row = tuple([row[col] for col in cols])
            if vals == vals_in_row:
                subset.add(index)
                break
    return subset

def comb(n: int, k: int) -> int:
    return int(factorial(n) / factorial(k) / factorial(n - k))

def locating_fitness(input_array):
    count = 0
    for i1, i2 in itertools.combinations(dset,2):                       #locating array compares two dsets
        s1 = set_iteration(input_array, i1)                             #if two dsets are occuring in any distinct row, then the array is not locating
        s2 = set_iteration(input_array, i2)
        if s1 != s2:
            if len(s1) != 0 and len(s2) != 0:                           #assumes d is equal to 1
                count += 1

    #--- Optimality ----#
    cov_count = (comb(k,t) * (v**t))
    opt = comb(cov_count, 2)
    return (count/opt)

def generator(num_rows, num_columns, num_values, num_arrays): #generates a random list of arrays with specified rows, columns, num values
    locating_obj_list = []
    for i in range(num_arrays): #generater will return a list containing num_arrays of arrays 
        array = []
        for row_num in range(num_rows):
            row = []
            for position in range(num_columns):
                row.append(random.randint(0,num_values-1))  #this is num_values - 1 b/c we have to account for zero Ie. (0,1) v = 2, but we only want 0s and 1s
            array.append(row)
        locating_obj_list.append(individual_array(array,locating_fitness(array)))
    return locating_obj_list

def to_file(num,array,count):
    full_path = os.path.join(path, f'[{num}]_{k}_{n}_{count}.txt')
    with open(full_path, 'w') as file:
        for row in array:
            file.write(' '.join([str(item) for item in row])) 
            file.write('\n')
def mutations(val, child):
    mutation = []   
    temp_child = child[:]                                                       #creating a copy to avoid locality issues
    if val == 1:                                                                #modify a row
        row_num = random.randint(0,n-1)
        mutation = [random.randint(0,v-1) for i in range(0,k)]                  #generate a random v-1 value k amount of times
        temp_child[row_num] = mutation
        mutated_child = temp_child
    if val == 2:
        column_num = random.randint(0,k-1)
        mutator = [random.randint(0,v-1) for i in range(0,n)]
        for num in range(len(mutator)):
            temp_child[num][column_num] = mutator[num]                        #modifies the value at {column_num} in each part of the 2d list 
        mutated_child = temp_child
    if val == 3:
        rand_val = random.randint(0,v-1)
        column_num = random.randint(0,k-1)      #picks random column in number of columns generated
        row_num = random.randint(0,n-1)         #picks random int in number of rows generated
        temp_child[row_num][column_num] = rand_val
        mutated_child = temp_child
    return mutated_child

def crossover(parent1, parent2, val):               #we need crossover to take in two lists and a val (0,1) to determine if 1 or 2 point crossover
    child = []
    if val == 1:                                    #one point crossover
        idx = random.randint(1,n-1) 
        for elem in parent1.array[:idx]: 
            child.append(elem[:])
        for elem in parent2.array[idx:]:
            child.append(elem[:])
    if val == 2:                                   #two point crossover
        idx1,idx2 = sorted(random.sample(range(1,n-1),2))             #ensure index 2 is always bigger than index 1
        for elem in parent1.array[:idx1]:
            child.append(elem[:])
        for elem in parent2.array[idx1:idx2]:
            child.append(elem[:])
        for elem in parent1.array[idx2:]:
            child.append(elem[:])      
    # print(parent1.fitness,parent2.fitness)
    # print(fit)
    return child


def basic_genetic_algo(n,k,v,pop_size,gen_count = 0):                                                                          
    list_algo_scope = generator(n,k,v,pop_size)
    temp_count = 0
    for i in range(1,51):                                                              #50 generations   
        temp_count += 1
        temp_list = []
        for p1 , p2 in itertools.combinations(list_algo_scope, 2):
            cross_percent = random.randint(1,10)
            mut_percent = random.randint(1,10)
            if len(temp_list) < 100:
                if cross_percent == 1 and mut_percent <= 3:                             #10% chance of crossover occuring and only want to go until 100 children have been produced
                    child = crossover(p1, p2, random.randint(1,2))
                    mutated_child = mutations(random.randint(1,3), child)
                    fitness = locating_fitness(mutated_child)
                    obj = individual_array(mutated_child,fitness)
                    if fitness == 1:
                        return obj, temp_count
                    else:
                        temp_list.append(obj)
                elif cross_percent == 1 and mut_percent > 3:
                    child = crossover(p1, p2, random.randint(1,2))
                    fitness = locating_fitness(child)
                    obj = individual_array(child,fitness)
                    if fitness == 1:
                        return obj, temp_count
                    else:
                        temp_list.append(obj)
        comb_list =  list_algo_scope + temp_list
        comb_list = sorted(comb_list, key = operator.attrgetter('fitness'))
        comb_list.reverse()
        list_algo_scope = comb_list[0:pop_size]                                         #picks the top 100   
    array, gen_count = basic_genetic_algo(n+1,k,v,pop_size,gen_count)                   #this is just a means to save this value
    return array, gen_count                                     


locating_array, count = basic_genetic_algo(n,k,v,pop_size)

def process_driver(p_id): 
    start_time = time.time()
    out, gen_count = basic_genetic_algo(n,k,v,pop_size)
    to_file((p_id+1),out.array,gen_count)
    print(f"%s Runtime: [{(p_id+1)}]_output_{k}_{n}_{gen_count}.txt Generated" % (time.time() - start_time))


if __name__ == "__main__":
    with multiprocessing.Pool(5) as p:
        p.map(process_driver, [0,1,2,3,4])

# RETIRED CODE ===========================================================================================================================================================================#
# !!!!!!!!!!!!!!!!!!!!!!!!
#   This determines if an array is covering, but is not really necessary for my later implementations.
# !!!!!!!!!!!!!!!!!!!!!!!!
# def covering_validator():
#     for cols in itertools.combinations(range(k),t):
#         s = set()
#         for row in ar:
#             val = tuple([row[col] for col in cols])
#             s.add(val)
#             if len(s) == v**t: break
#         else:
#             return False
#     return  True
#
# !!!!!!!!!!!!!!!!!!!!!!!!
#   This was how we initially read in a covering array, but is no longer necessary.
# !!!!!!!!!!!!!!!!!!!!!!!!        
#with open('test.txt') as f:
#    ar = [list(map(int,line.split())) for line in f.readlines()]


#k = number of columns; v = number of values; t = strength(how many columns are being compared) d = interaction between interactions


# def add_line(n,k,v,pop_size):                                                         #main_loop tests locating fitness on every array in the list
#     locating = False 
#     while locating == False:
#         print(n)
#         array_list = generator(n,k,v,pop_size)                                        #this is the starting array list produced by the generator
#         print('regen')
#         for ar in array_list:
#             fitness = locating_fitness(ar)
#             if fitness == 1:
#                 locating = True
#                 return ar
#         print('here')
#         n += 1                                                                      #adds a row if it makes it through the full iteration without generating a locating array                                                                            #adds a row if it makes it through the full iteration without generating a locating array
