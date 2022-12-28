INTRODUCTION:

The purpose of this repo is to present a basic genetic algorithm which is designed to create a 2D-Array (implemented with nested lists in python) which can be 
classified as a locating array. Locating arrays build upon covering arrays - arrays which cover every interaction between any given column. A (d,t) locating array
allows any set of interaction faults to be found given there are at most (d) faults, and (t) interactions.


    COVERING       COVERING &
  NOT LOCATING     LOCATING
    0 0 0 0    |    0 1 1 0
    0 1 1 1    |    1 0 1 1
    1 0 1 1    |    1 1 1 0 
    1 1 0 1    |    0 1 1 1     
    1 1 1 0    |    0 0 0 1
               |    1 0 0 0 
               |    0 0 1 0
               |    1 1 0 1
        

The array on the left covers every possible interaction, but does not allow us to locate if there are any faults. To explain further, if the outcome of each row was
to either pass or fail, and the output of row 1 in the Non-Locating array failed, there would be no way to isolate the interaction that caused it. The Additional
rows in the Locating array on the right provide the necessary cases to ensure all interactions are covered. 

These variables are listed below:

t = #num of columns in interaction
v = #num of values    
d = #the size of the set of interactions              
k = #num of columns
n = #starting num of rows

We used a genetic algorithm whose representation is N*k. It generates a new child every 5 seconds if a locating array has not been created yet.
With at least two arrays, the algorithm will continue to generate children until a locating array with 100% accuracy is produced or 300 seconds pass - whichever happens first.

pop_size = # population size

HOW TO USE:

These variable assignments will be seen immediately upon opening the code:

t = 2  #num of columns in interaction
v = 2  #num of values    
d = 1  #num of d interactions (interaction of interactions) 
k = 4 #num of columns
n = 8 #starting num of rows
pop_size = 10 # population size                                     

Variables can be changed by hand to test different size arrays, different amounts of values, and different interactions. Upon completing, the locating array will be printed to a file called [x]_{k}_{n}_{t}.txt 
where the corresponding variables run in the file are reflected by the file name and where x is a number from 1-25. Each time the program runs, it creates 25 output files
creates a corresponding directory tilted {k}_{n}_{t}. The repo has tests further seperated in labeled directories.

HOW TO RUN: in command line > python3 ./locating_array_validator.py 

Additionally, there is a stats.py program which can be run to see the median, mode, mean, min, and max number of rows produced for a given directory. This allows you to input one of the produced directories,
and find the average amount of rows in all of the succesful locating arrays.

HOW TO RUN: python3 ./stats.py

It well then prompt the user for the directory it would like to access. Type the name (ex. 8_44_3) and it will print out the required stats.

Note: Changing the d value in specific will likely make it almost impossible to observe an output efficiently. The option is there as I hope to make the algorithm
efficient enough to change this at some point. Additionally, the lower the starting arrays and rows are, the less likely an optimal output is to be observed.
