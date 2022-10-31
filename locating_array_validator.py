import itertools
import math
import random
import copy

t = 2  #num of columns in interaction
v = 2  #num of values    
d = 1  #num of d interactions (interaction of interactions) 
k = 4  #num of columns
n = 8  #starting num of rows
x = 100 #number of arrays to generate
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


def main_loop(n,k,v,x):   #main_loop tests locating fitness on every array in the list
    locating = False 
    while locating == False:
        array_list = generator(n,k,v,x) #this is the starting array list produced by the generator
        for ar in array_list:
            fitness = locating_fitness(ar)
            if fitness == 1:
                locating = True
                return ar 
        n += 1          #adds a row if it makes it through the full iteration without generating a locating array

def to_file(array):
    with open('output.txt', 'w') as file:
        for row in array:
            file.write(' '.join([str(item) for item in row]))
            file.write('\n') 


array_list = generator(n,k,v,x)

def basic_genetic_algo(list):
    locating = False
    list_algo_scope = copy.deepcopy(list) 
    print(list_algo_scope)
    print("SEPERATOR ------------------------------------------------------")
    def breeding(list): #takes in list of arrays
        parent1 = random.choice(list) #picks random array in list
        parent2 = random.choice(list) #picks random array in list
        child = []
        idx = random.randint(0,n) 
        for elem in parent1[:idx]: 
            child.append(elem)
        for elem in parent2[idx:]:
            child.append(elem)
        if locating_fitness(child) <= (locating_fitness(parent1) or locating_fitness(parent2)):
            pass
        else:
            list.append(child)
    while locating == False:
        breeding(list_algo_scope)
        print(locating_fitness(list_algo_scope[-1]))
        if locating_fitness(list_algo_scope[-1]) == 1:
            locating = True
            return list_algo_scope[-1]


print(basic_genetic_algo(array_list))
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