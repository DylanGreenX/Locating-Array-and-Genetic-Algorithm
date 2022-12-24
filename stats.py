import os
import statistics

data = []
name = input("what folder do you want the path to? \n")
for filename in os.listdir(os.getcwd()+f"/{name}"):
    with open(os.path.join(os.getcwd()+f"/{name}", filename), 'r') as f: # open in readonly mode
      data.append(len(f.readlines()))


# Finding Mean
print("\nMean: ", statistics.mean(data))
# Finding Median
print("Median: ", statistics.median(data))
# Finding Mode
print("Mode: ", statistics.mode(data))
#Finding Min
print("Min: ", min(data))

#Finding Max
print("Min: ", max(data))