import itertools
import math
import random
import copy
import time
import os
start_time = time.time()


t = 2  #num of columns in interaction
v = 2  #num of values    
d = 1  #the size of the set of interactions
k = 4  #num of columns
n = 8  #starting num of rows
pop_size = 10 # population size
#Random Array Generation

def generator(num_rows, num_columns, num_values, num_arrays): #generates a random list of arrays with specified rows, columns, num values
    array_list = []
    for i in range(num_arrays): #generater will return a list containing num_arrays of arrays 
        array = []
        for row_num in range(num_rows):
            row = []
            for position in range(num_columns):
                row.append(random.randint(0,num_values-1))  #this is num_values - 1 b/c we have to account for zero Ie. (0,1) v = 2, but we only want 0s and 1s
            array.append(row)
        array_list.append(array)
    return array_list


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

def locating_fitness(input_array):
    count = 0
    for i1, i2 in itertools.combinations(dset,2):                       #locating array compares two dsets
        s1 = set_iteration(input_array, i1)                             #if two dsets are occuring in any distinct row, then the array is not locating
        s2 = set_iteration(input_array, i2)
        if s1 != s2:
            count += 1

    #--- Optimality ----#
    cov_count = (math.comb(k,t) * (v**t))
    opt = math.comb(cov_count, 2)
    return (count/opt)


def add_line(n,k,v,pop_size):                                                         #main_loop tests locating fitness on every array in the list
    locating = False 
    while locating == False:
        print(n)
        array_list = generator(n,k,v,pop_size)                                        #this is the starting array list produced by the generator
        print('regen')
        for ar in array_list:
            fitness = locating_fitness(ar)
            if fitness == 1:
                locating = True
                return ar
        print('here')
        n += 1                                                                 #adds a row if it makes it through the full iteration without generating a locating array                                                                            #adds a row if it makes it through the full iteration without generating a locating array

def to_file(array):
    with open(f'output_{t}_{k}_{v}_{d}_{n}.txt', 'w') as file:
        for row in array:
            file.write(' '.join([str(item) for item in row]))
            file.write('\n') 

def mutations(val, child):
    mutation = []   
    temp_child = child[:]                                                       #creating a copy to avoid locality issues
    for i in temp_child: print(f"{i}")
    print("\n")
    if val == 1:                                                                #modify a row
        row_num = random.randint(0,n-1)
        print(f"i will modify row {row_num}")
        mutation = [random.randint(0,v-1) for i in range(0,k)]                  #generate a random v-1 value k amount of times
        temp_child[row_num] = mutation
        mutated_child = temp_child
    if val == 2:
        column_num = random.randint(0,k-1)
        print(f"i will modify col {column_num}")
        mutator = [random.randint(0,v-1) for i in range(0,n)]
        for num in range(len(mutator)):
            temp_child[num][column_num] = mutator[num]                        #modifies the value at {column_num} in each part of the 2d list 
        mutated_child = temp_child
    if val == 3:
        rand_val = random.randint(0,v-1)
        column_num = random.randint(0,k-1)     #picks random column in number of columns generated
        row_num = random.randint(0,n-1)     #picks random int in number of rows generated
        print(f"i will modify {row_num},{column_num}")
        temp_child[row_num][column_num] = rand_val
        mutated_child = temp_child
    print("----------------------\n")
    for i in mutated_child: print(f"{i}") 
    print("\n")
    return mutated_child

def crossover(parent1, parent2, val):               #we need crossover to take in two lists and a val (0,1) to determine if 1 or 2 point crossover
    child = []
    if val == 1:                                    #one point crossover
        idx = random.randint(0,n) 
        for elem in parent1[:idx]: 
            child.append(elem[:])
        for elem in parent2[idx:]:
            child.append(elem[:])
    if val == 2:                                   #two point crossover
        idx1,idx2 = sorted(random.sample(range(0,n),2))             #ensure index 2 is always bigger than index 1
        for elem in parent1[:idx1]: 
            child.append(elem[:])
        for elem in parent2[idx1:idx2]:
            child.append(elem[:])
        for elem in parent2[idx2:]:
            child.append(elem[:])      
    return child

def basic_genetic_algo(n,k,v,pop_size):
    locating = False
    list_algo_scope = generator(n,k,v,pop_size)
    def breeding(list):                                                         #takes in list of arrays
        mut_num = random.randint(1,3)                                        #determining what number mutation to use
        parent1, parent2 = random.sample(list_algo_scope, k = 2)                #picks random array in list
        child = mutations(mut_num,crossover(parent1,parent2,random.randint(1,2)))
        list.append(child)
    loop_time = time.time()
    while locating == False:
        breeding(list_algo_scope)
        fitness = locating_fitness(list_algo_scope[-1])
        if fitness == 1:            
            return list_algo_scope[-1]
        if time.time() - loop_time > 5.0:
            break
    if time.time() - start_time > 60:
        print("Generation Limit: 100% coverage not found in 60 seconds")
        quit()
    return basic_genetic_algo(n+1,k,v,pop_size)



start_time = time.time()
out = basic_genetic_algo(n,k,v,pop_size)
to_file(out)
print(f"%s Runtime: output_{t}_{k}_{v}_{d}_{n}.txt Generated" % (time.time() - start_time))


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
