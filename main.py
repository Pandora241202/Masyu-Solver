from timeit import default_timer as timer
import json
import masyu
import tracemalloc

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
        puzzel = masyu.Masyu(int(sizeStr), nodes)
        
        print("")
        print("Puzzel:")
        print("")
        puzzel.printState({})
        
        print("")
        print("Choose solving option:")
        print("Depth-First Search: 1")
        print("Heuristic Search with Backtracking: 2")
        option = input()
        solver = None
        if int(option) == 2:
            print("\nSolution using Heuristic Search with Backtracking:")
            solver = masyu.MasyuHeuristicSolver(puzzel)
        if int(option) == 1:
            print("\nSolution using Depth-First Search:")
            solver = masyu.MasyuDFSSolver(puzzel)
            
        start = timer()
        tracemalloc.start()
        puzzel.printState(solver.solve())
        print("--- %s B ---" % tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
        with open("solution.txt", "a") as file:  
            file.write("--- %s seconds ---" % (timer() - start))
        print("--- %s seconds ---" % (timer() - start))

if __name__ == "__main__":
    main()