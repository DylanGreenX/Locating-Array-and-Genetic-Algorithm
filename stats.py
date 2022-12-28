import os
import statistics

data = []
name = input("what folder do you want the path to? \n")
for filename in os.listdir(os.getcwd()+f"/{name}"):
    with open(os.path.join(os.getcwd()+f"/{name}", filename), 'r') as f: # open in readonly mode
      data.append(len(f.readlines()))


# Finding Median
print("\nMedian: ", statistics.median(data))
# Finding Mode
print("Mode: ", statistics.mode(data))
#Finding Min
print("\nMin: ", min(data))
# Finding Mean
print("Mean: ", statistics.mean(data))
#Finding Max
print("Max: ", max(data))