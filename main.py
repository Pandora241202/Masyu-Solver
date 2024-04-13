from timeit import default_timer as timer
import json
from masyu import Masyu

BLACK = 0
WHITE = 1
          
def tuple_hook(dct):
    new_dict = {}
    for key, value in dct.items():
        new_key = tuple(map(int, key.strip('()').split(',')))
        new_dict[new_key] = value
    return new_dict

def main():
    while True:
        sizeStr = input("Enter Masyu-puzzel size (6,8,10,15,20,25): ")
        i = input("Enter index: ") 
        nodes = {}
        with open(sizeStr + "x" + sizeStr + "/" + i + ".txt", "r") as f:
            nodes = json.load(f, object_hook=tuple_hook)
        puzzel = Masyu(int(sizeStr), nodes)
        
        print("")
        print("Puzzel:")
        print("")
        puzzel.printState({})
        
        print("")
        print("Choose solving option:")
        print("DFS: 1")
        print("What: 2")
        option = input()
        if int(option) == 2:
            start = timer()
            puzzel.solveWithWhat()
            with open("solution.txt", "a") as file:  
                file.write("--- %s seconds ---" % (timer() - start))
            print("--- %s seconds ---" % (timer() - start))

if __name__ == "__main__":
    main()