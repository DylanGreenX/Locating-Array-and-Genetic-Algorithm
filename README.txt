INTRODUCTION:

The purpose of this repo is to present a basic genetic algorithm which is designed to create a 2D-Array (implemented with nested lists in python) which can be 
classified as a locating array. A locating array is one in which covers every possible interaction between a given set of values across each column. A simple example 
can be seen below:


NOT LOCATING     |     LOCATING
---------------  | ----------------
0 1              |    0 1
1 0              |    1 0
0 0              |    0 0
1 0              |    1 1
                 |
---------------  | ----------------
Missing             All 
Interaction (1 1)   Interactions Seen
(75% Optimal)       (100% Optimal)


Though this is a very simple example with only two columns this array on the left would not be locating because not every possible interaction is observed. 
There are multiple variables that can be changed however, to increasing the number of observable values, the number of columns, the number of rows, and
the number of interactions.

These variables are listed below:

t = #num of columns in interaction
v = #num of values    
d = #num of d interactions (interaction of interactions)                    // These variables are reflected in the code
k = #num of columns
n = #starting num of rows

Our genetic algorithm seeks to generate arrays that are classified as locating while maintaining as few rows as possible (to be comperable to that of other algorithms).
In doing so we start with a given amount of randomly generated arrays, and then generate a child array - mutating one row in the child at random. We set a random a 
predetermined amount of arrays to start our genetic algorithm. With at least two arrays, the algorithm will continue to run until it generates a child with 100% 
accuracy.

x = #number of arrays to generate                                       // This variable is reflected in the code

HOW TO USE:

These variable assignments will be seen immediately upon opening the code:

t = 2  #num of columns in interaction
v = 2  #num of values    
d = 1  #num of d interactions (interaction of interactions) 
k = 20 #num of columns
n = 50 #starting num of rows
x = 10 #number of arrays to generate                                      

Variables can be changed by hand to test different size arrays, different amounts of values, and different interactions. Upon completing, a runtime will be printed
and the locating array will be printed to a file called output.txt. (There is an example output reflecting the above variables in the repo as well).

Note: Changing the d value in specific will likely make it almost impossible to observe an output efficiently. The option is there as I hope to make the algorithm
efficient enough to change this at some point. Additionally, the lower the starting arrays and rows are, the less likely an optimal output is to be observed.
