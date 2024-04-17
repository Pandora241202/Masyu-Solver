import copy

class Masyu:
    WHITE = 1
    BLACK = 0

    def __init__(self, size: int, nodes: dict[tuple[int, int], int]):
        self.size = size
        self.nodes = nodes

    def printState(self, ajdList: dict[tuple[int, int], list[tuple[int, int]]]):
        i = 0
        for i in range(self.size - 1):
            j = 0
            for j in range(self.size - 1):
                if (i, j) in self.nodes:
                    print("O" if self.nodes[(i,j)] == Masyu.WHITE else "@", end="")
                else:
                    print(".", end="")
                if (i, j) in ajdList and (i, j+1) in ajdList[(i, j)]:
                    print("----", end="")
                else:
                    print("    ", end="")
            j = j+1
            if (i, j) in self.nodes:
                print("O" if self.nodes[(i,j)] == Masyu.WHITE else "@")
            else:
                print(".")
            j = 0
            for j in range(self.size):
                if (i, j) in ajdList and (i+1, j) in ajdList[(i, j)]:
                    print("|    ", end="")
                else:
                    print("     ", end="")
            print("")
        j = 0
        i = i+1
        for j in range(self.size - 1):
            if (i, j) in self.nodes:
                print("O" if self.nodes[(i,j)] == Masyu.WHITE else "@", end="")
            else:
                print(".", end="")
            if (i, j) in ajdList and (i, j+1) in ajdList[(i, j)]:
                print("----", end="")
            else:
                print("    ", end="")
        j = j + 1
        if (i, j) in self.nodes:
            print("O" if self.nodes[(i,j)] == Masyu.WHITE else "@")
        else:
            print(".")
            
    def printStateToFile(self, ajdList: dict[tuple[int, int], list[tuple[int, int]]], fileName: str):
        if self.size >= 15:
            return
        with open(fileName, "a") as f:
            i = 0
            for i in range(self.size - 1):
                j = 0
                for j in range(self.size - 1):
                    if (i, j) in self.nodes:
                        f.write("O" if self.nodes[(i,j)] == Masyu.WHITE else "@")
                    else:
                        f.write(".")
                    if (i, j) in ajdList and (i, j+1) in ajdList[(i, j)]:
                        f.write("----")
                    else:
                        f.write("    ")
                j = j+1
                if (i, j) in self.nodes:
                    f.write("O" if self.nodes[(i,j)] == Masyu.WHITE else "@")
                    f.write("\n")
                else:
                    f.write(".\n")
                j = 0
                for j in range(self.size):
                    if (i, j) in ajdList and (i+1, j) in ajdList[(i, j)]:
                        f.write("|    ")
                    else:
                        f.write("     ")
                f.write("\n")
            j = 0
            i = i+1
            for j in range(self.size - 1):
                if (i, j) in self.nodes:
                    f.write("O" if self.nodes[(i,j)] == Masyu.WHITE else "@")
                else:
                    f.write(".")
                if (i, j) in ajdList and (i, j+1) in ajdList[(i, j)]:
                    f.write("----")
                else:
                    f.write("    ")
            j = j + 1
            if (i, j) in self.nodes:
                f.write("O" if self.nodes[(i,j)] == Masyu.WHITE else "@")
                f.write("\n")
            else:
                f.write(".\n")
            f.write("\n")

    def isValidPos(self, pos: tuple[int, int]):
        if not pos: 
            return False
        return pos[0] >= 0 and pos[0] < self.size and pos[1] >= 0 and pos[1] < self.size

    def threePosStraight(self, pos1: tuple[int, int], midPos: tuple[int, int], pos2: tuple[int, int]):
        return pos1[0] == 2*midPos[0] - pos2[0] and pos1[1] == 2*midPos[1] - pos2[1]
    
    def getLeft(self, pos: tuple[int, int]):
        return None if pos[0]-1 < 0 else (pos[0]-1, pos[1])
    
    def getRight(self, pos: tuple[int, int]):
        return None if pos[0]+1 == self.size else (pos[0]+1, pos[1])
    
    def getTop(self, pos: tuple[int, int]):
        return None if pos[1]-1 < 0 else (pos[0], pos[1]-1)
    
    def getBot(self, pos: tuple[int, int]):
        return None if pos[1]+1 == self.size else (pos[0], pos[1]+1)

    def connect2Pos(self, pos1: tuple[int, int], pos2: tuple[int, int], ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        if pos1 not in ajdList: ajdList[pos1] = []
        if pos2 not in ajdList: ajdList[pos2] = []
        if pos2 not in ajdList[pos1]:
            ajdList[pos1].append(pos2)
            ajdList[pos2].append(pos1)

    def delConnect2Pos(self, pos1: tuple[int, int], pos2: tuple[int, int], ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        ajdList[pos1].remove(pos2)
        if len(ajdList[pos1]) == 0:
            ajdList.pop(pos1)
        ajdList[pos2].remove(pos1)
        if len(ajdList[pos2]) == 0:
            ajdList.pop(pos2)

    def checkLocalLoopFromConnect(self, pos1: tuple[int, int], pos2: tuple[int, int], ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        prePos = pos2
        curPos = ajdList[pos2][0]
        count = 2 if pos1 in self.nodes and pos2 in self.nodes else (1 if pos1 in self.nodes or pos2 in self.nodes else 0)
        while curPos != pos1:
            if len(ajdList[curPos]) == 1: return False
            if curPos in self.nodes:
                count += 1
            t = curPos
            curPos = ajdList[curPos][0] if ajdList[curPos][0] != prePos else ajdList[curPos][1]
            prePos = t
        return count < len(self.nodes)

    def check2StraightLinesAfterWhiteNodes(self, prePos: tuple[int, int], whitePos: tuple[int, int], ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        if whitePos not in ajdList or len(ajdList[whitePos]) == 1:
            return False
        midP = ajdList[whitePos][0] if not prePos or ajdList[whitePos][0] != prePos else ajdList[whitePos][1]
        if len(ajdList[midP]) == 1:
            return False
        p2 = ajdList[midP][0] if ajdList[midP][0] != whitePos else ajdList[midP][1]
        return self.threePosStraight(whitePos, midP, p2)
        
    def isLegalConnect(self, pos: tuple[int, int], connectPos: tuple[int, int], ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        # pos is guaranteed to be valid
        if not self.isValidPos(connectPos):
            return False

        # pos is guaranteed to have less than 2 connections
        if connectPos in ajdList and len(ajdList[connectPos]) > 1:
            return False
        
        if pos in ajdList and ajdList[pos][0] in self.nodes:
            # Turn before or after black node not allowed
            if self.nodes[ajdList[pos][0]] == Masyu.BLACK and not self.threePosStraight(ajdList[pos][0], pos, connectPos):
                return False
            if self.nodes[ajdList[pos][0]] == Masyu.WHITE and self.threePosStraight(connectPos, pos, ajdList[pos][0]):
                # 2 straight lines before and after white node not allowed
                if self.check2StraightLinesAfterWhiteNodes(pos, ajdList[pos][0], ajdList):
                    return False
                # 2 straight lines after 2 white nodes not allowed
                if (2*ajdList[pos][0][0]-pos[0], 2*ajdList[pos][0][1]-pos[1]) in self.nodes and self.nodes[(2*ajdList[pos][0][0]-pos[0], 2*ajdList[pos][0][1]-pos[1])] == Masyu.WHITE:
                    return False
        
        if connectPos not in ajdList:
            if connectPos not in self.nodes:
                return True
            # Try to connect white node which current has no connections
            if self.nodes[connectPos] == Masyu.WHITE:
                # Turn before reach white node
                if pos not in ajdList or not self.threePosStraight(ajdList[pos][0], pos, connectPos):
                    return True
                # Straight line before reach white node allowed only if white node with no node after or black node after
                return (2*connectPos[0]-pos[0], 2*connectPos[1]-pos[1]) not in self.nodes or self.nodes[(2*connectPos[0]-pos[0], 2*connectPos[1]-pos[1])] == Masyu.BLACK
            # Only straight line before black node allowed 
            return pos not in ajdList or self.threePosStraight(connectPos, pos, ajdList[pos][0])
        
        if pos in self.nodes:
            if self.nodes[pos] == Masyu.WHITE and self.threePosStraight(pos, connectPos, ajdList[connectPos][0]) and self.check2StraightLinesAfterWhiteNodes(None, pos, ajdList):
                return False
            if self.nodes[pos] == Masyu.BLACK and not self.threePosStraight(pos, connectPos, ajdList[connectPos][0]):
                return False
        
        if pos in ajdList and self.checkLocalLoopFromConnect(pos, connectPos, ajdList):
            return False 
        
        if connectPos not in self.nodes:
            if ajdList[connectPos][0] not in self.nodes:
                return True
            if self.nodes[ajdList[connectPos][0]] == Masyu.BLACK:
                return self.threePosStraight(pos, connectPos, ajdList[connectPos][0])
            if not self.threePosStraight(pos, connectPos, ajdList[connectPos][0]):
                return True
            return not self.check2StraightLinesAfterWhiteNodes(connectPos, ajdList[connectPos][0], ajdList)
        if self.nodes[connectPos] == Masyu.WHITE:
            # Make a turn at white node
            if not self.threePosStraight(pos, connectPos, ajdList[connectPos][0]):
                return False
            # Turn at pos right before reach white node
            if pos in ajdList and not self.threePosStraight(ajdList[pos][0], pos, connectPos):
                return True
            # Straight line before reach white node with 1 line after
            return not self.check2StraightLinesAfterWhiteNodes(None, connectPos, ajdList)
        # Straight line pass black node
        if self.threePosStraight(pos, connectPos, ajdList[connectPos][0]):
            return False
        # Straight line before black node and turn at black node
        if pos not in ajdList or self.threePosStraight(ajdList[pos][0], pos, connectPos):
            return True
        # Turn right before reach black node
        return False        

    def makeLegalConnectsFromPos(self, pos: tuple[int, int], ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        connectPos = []        
        if pos in self.nodes:
            if pos not in ajdList:
                if self.nodes[pos] == Masyu.WHITE:
                    # White node can't make connection to 2 ajadent directions
                    if (not self.isLegalConnect(pos, self.getLeft(pos), ajdList) or not self.isLegalConnect(pos, self.getRight(pos), ajdList)) and (not self.isLegalConnect(pos, self.getTop(pos), ajdList) or not self.isLegalConnect(pos, self.getBot(pos), ajdList)):
                        return []
                    if not self.isLegalConnect(pos, self.getLeft(pos), ajdList) or not self.isLegalConnect(pos, self.getRight(pos), ajdList):
                        return [self.getTop(pos)]
                    if not self.isLegalConnect(pos, self.getTop(pos), ajdList) or not self.isLegalConnect(pos, self.getBot(pos), ajdList):
                        return [self.getLeft(pos)]
                    return [self.getTop(pos), self.getLeft(pos)]
                if (not self.isLegalConnect(pos, self.getLeft(pos), ajdList) and not self.isLegalConnect(pos, self.getRight(pos), ajdList)) or (not self.isLegalConnect(pos, self.getTop(pos), ajdList) and not self.isLegalConnect(pos, self.getBot(pos), ajdList)):
                    return []
                if not self.isLegalConnect(pos, self.getBot(pos), ajdList):
                    return [self.getTop(pos)]
                if not self.isLegalConnect(pos, self.getTop(pos), ajdList):
                    return [self.getBot(pos)]   
                if not self.isLegalConnect(pos, self.getLeft(pos), ajdList):
                    return [self.getRight(pos)]
                if not self.isLegalConnect(pos, self.getRight(pos), ajdList):
                    return [self.getLeft(pos)]  
                return [self.getTop(pos), self.getLeft(pos)]
                
            if self.nodes[pos] == Masyu.WHITE:
                return [(2*pos[0] - ajdList[pos][0][0], 2*pos[1] - ajdList[pos][0][1])] if self.isLegalConnect(pos, (2*pos[0] - ajdList[pos][0][0], 2*pos[1] - ajdList[pos][0][1]), ajdList) else []
            else:
                # Black node current connect to same row pos
                if ajdList[pos][0][0] == pos[0]:
                    if self.isLegalConnect(pos, (pos[0]+1, pos[1]), ajdList):
                        connectPos = [(pos[0]+1, pos[1])] + connectPos if (pos[0]+1, pos[1]) in self.nodes else connectPos + [(pos[0]+1, pos[1])]
                    if self.isLegalConnect(pos, (pos[0]-1, pos[1]), ajdList):
                        connectPos = [(pos[0]-1, pos[1])] + connectPos if (pos[0]-1, pos[1]) in self.nodes else connectPos + [(pos[0]-1, pos[1])]
                # Black node current connect to same col pos
                else:
                    if self.isLegalConnect(pos, (pos[0], pos[1]-1), ajdList):
                        connectPos = [(pos[0], pos[1]-1)] + connectPos if (pos[0], pos[1]-1) in self.nodes else connectPos + [(pos[0], pos[1]-1)]
                    if self.isLegalConnect(pos, (pos[0], pos[1]+1), ajdList):
                        connectPos = [(pos[0], pos[1]+1)] + connectPos if (pos[0], pos[1]+1) in self.nodes else connectPos + [(pos[0], pos[1]+1)]
        else:
            if pos in ajdList:
                if self.getLeft(pos) != ajdList[pos][0] and self.isLegalConnect(pos, self.getLeft(pos), ajdList):
                    connectPos = [self.getLeft(pos)] + connectPos if self.getLeft(pos) in self.nodes else connectPos + [self.getLeft(pos)]
                if self.getRight(pos) != ajdList[pos][0] and self.isLegalConnect(pos, self.getRight(pos), ajdList):
                    connectPos = [self.getRight(pos)] + connectPos if self.getRight(pos) in self.nodes else connectPos + [self.getRight(pos)]
                if self.getTop(pos) != ajdList[pos][0] and self.isLegalConnect(pos, self.getTop(pos), ajdList):
                    connectPos = [self.getTop(pos)] + connectPos if self.getTop(pos) in self.nodes else connectPos + [self.getTop(pos)]
                if self.getBot(pos) != ajdList[pos][0] and self.isLegalConnect(pos, self.getBot(pos), ajdList):
                    connectPos = [self.getBot(pos)] + connectPos if self.getBot(pos) in self.nodes else connectPos + [self.getBot(pos)]
            else:
                if self.isLegalConnect(pos, self.getLeft(pos), ajdList):
                    connectPos = [self.getLeft(pos)] + connectPos if self.getLeft(pos) in self.nodes else connectPos + [self.getLeft(pos)]
                if self.isLegalConnect(pos, self.getRight(pos), ajdList):
                    connectPos = [self.getRight(pos)] + connectPos if self.getRight(pos) in self.nodes else connectPos + [self.getRight(pos)]
                if self.isLegalConnect(pos, self.getTop(pos), ajdList):
                    connectPos = [self.getTop(pos)] + connectPos if self.getTop(pos) in self.nodes else connectPos + [self.getTop(pos)]
                if self.isLegalConnect(pos, self.getBot(pos), ajdList):
                    connectPos = [self.getBot(pos)] + connectPos if self.getBot(pos) in self.nodes else connectPos + [self.getBot(pos)]

        return connectPos

    def isGoal(self, ajdList:dict[tuple[int, int], list[tuple[int,int]]]):
        if len(ajdList) < len(self.nodes): return False

        end = ()
        for pos in self.nodes:
            end = pos
            if end not in ajdList:
                return False
            break

        prePos = end
        curPos = ajdList[end][0]
        count = 1
        while curPos != end:
            if len(ajdList[curPos]) == 1:
                return False
            if curPos in self.nodes:

                count += 1
            t = curPos
            curPos = ajdList[curPos][0] if ajdList[curPos][0] != prePos else ajdList[curPos][1]
            prePos = t

        return count == len(self.nodes)


class MasyuHeuristicSolver:
    def  __init__(self, puzzel: Masyu):
        self.puzzel = puzzel
        self.ajdList: dict[tuple[int, int], list[tuple[int,int]]] = {}
       
    def preprocessing(self):
        for pos in self.puzzel.nodes:
            # For white nodes
            if self.puzzel.nodes[pos] == Masyu.WHITE:
                # White node at edge
                # Vertical
                if pos[1] == 0 or pos[1] == self.puzzel.size - 1:
                    self.puzzel.connect2Pos(pos, (pos[0]-1, pos[1]), self.ajdList)
                    self.puzzel.connect2Pos(pos, (pos[0]+1, pos[1]), self.ajdList)
                # Horizontal
                if pos[0] == 0 or pos[0] == self.puzzel.size - 1:
                    self.puzzel.connect2Pos(pos, (pos[0], pos[1]-1), self.ajdList)
                    self.puzzel.connect2Pos(pos, (pos[0], pos[1]+1), self.ajdList)

                # >=3 white node next to each other
                # Horizontal
                countContinuWhiteNodes = 1
                while pos[1] + countContinuWhiteNodes < self.puzzel.size:
                    if (pos[0], pos[1] + countContinuWhiteNodes) not in self.puzzel.nodes or self.puzzel.nodes[(pos[0], pos[1] + countContinuWhiteNodes)] == Masyu.BLACK:
                        break
                    countContinuWhiteNodes += 1
                if countContinuWhiteNodes >= 3:
                    for i in range(countContinuWhiteNodes):
                        self.puzzel.connect2Pos((pos[0], pos[1]+i), (pos[0]-1, pos[1]+i), self.ajdList)
                        self.puzzel.connect2Pos((pos[0], pos[1]+i), (pos[0]+1, pos[1]+i), self.ajdList)
                # Vertical
                countContinuWhiteNodes = 1
                while pos[0] + countContinuWhiteNodes < self.puzzel.size:
                    if (pos[0] + countContinuWhiteNodes, pos[1]) not in self.puzzel.nodes or self.puzzel.nodes[(pos[0] + countContinuWhiteNodes, pos[1])] == Masyu.BLACK:
                        break
                    countContinuWhiteNodes += 1
                if countContinuWhiteNodes >= 3:
                    for i in range(countContinuWhiteNodes):
                        self.puzzel.connect2Pos((pos[0]+i, pos[1]), (pos[0]+i, pos[1]-1), self.ajdList)
                        self.puzzel.connect2Pos((pos[0]+i, pos[1]), (pos[0]+i, pos[1]+1), self.ajdList)

            # For black nodes
            else:
                # Black node at edge or distance to edge = 1
                # Horizontal
                if pos[1] == 0 or pos[1] == self.puzzel.size - 1 or pos[1] == 1 or pos[1] == self.puzzel.size - 2:
                    connectPos = (pos[0], pos[1]+1 if pos[1] == 0 or pos[1] == 1 else pos[1]-1)
                    self.puzzel.connect2Pos(pos, connectPos, self.ajdList)
                    self.puzzel.connect2Pos(connectPos, (connectPos[0], connectPos[1]+1 if pos[1] == 0 or pos[1] == 1 else connectPos[1]-1), self.ajdList)
                # Vertical
                if pos[0] == 0 or pos[0] == self.puzzel.size - 1 or pos[0] == 1 or pos[0] == self.puzzel.size - 2:
                    connectPos = (pos[0] + 1 if pos[0] == 0 or pos[0] == 1 else pos[0]-1, pos[1])
                    self.puzzel.connect2Pos(pos, connectPos, self.ajdList)
                    self.puzzel.connect2Pos(connectPos, (connectPos[0] + 1 if pos[0] == 0 or pos[0] == 1 else connectPos[0]-1, connectPos[1]), self.ajdList)

                # 2 black nodes next to each other
                # Horizontal
                if (pos[0], pos[1]+1) in self.puzzel.nodes and self.puzzel.nodes[(pos[0], pos[1]+1)] == Masyu.BLACK:
                    self.puzzel.connect2Pos(pos, (pos[0], pos[1]-1), self.ajdList)
                    self.puzzel.connect2Pos((pos[0], pos[1]-1), (pos[0], pos[1]-2), self.ajdList)
                    self.puzzel.connect2Pos((pos[0], pos[1]+1), (pos[0], pos[1]+2), self.ajdList)
                    self.puzzel.connect2Pos((pos[0], pos[1]+2), (pos[0], pos[1]+3), self.ajdList)
                # Vertical
                if (pos[0]+1, pos[1]) in self.puzzel.nodes and self.puzzel.nodes[(pos[0]+1, pos[1])] == Masyu.BLACK:
                    self.puzzel.connect2Pos(pos, (pos[0]-1, pos[1]), self.ajdList)
                    self.puzzel.connect2Pos((pos[0]-1, pos[1]), (pos[0]-2, pos[1]), self.ajdList)
                    self.puzzel.connect2Pos((pos[0]+1, pos[1]), (pos[0]+2, pos[1]), self.ajdList)
                    self.puzzel.connect2Pos((pos[0]+2, pos[1]), (pos[0]+3, pos[1]), self.ajdList)

        self.puzzel.printStateToFile(self.ajdList, "solution.txt")

    def backtrackWithHeuristic(self):

        self.puzzel.printStateToFile(self.ajdList, "solution.txt")

        if self.puzzel.isGoal(self.ajdList):
            return True

        tryMoves = None
        # Try to continue lines in current state
        for pos in self.ajdList:
            if len(self.ajdList[pos]) == 1:
                legalMoves = self.puzzel.makeLegalConnectsFromPos(pos, self.ajdList)
                if len(legalMoves) == 0:
                    return False
                # Find pos with least options to be chosen
                if not tryMoves:
                    tryMoves = (pos, legalMoves)
                else:
                    if (len(legalMoves) < len(tryMoves[1])) or (len(legalMoves) == len(tryMoves[1]) and tryMoves[1][0] in self.puzzel.nodes):
                        tryMoves = (pos, legalMoves)
        # Try to find move from nodes
        for pos in self.puzzel.nodes:
            if pos not in self.ajdList:
                legalMoves = self.puzzel.makeLegalConnectsFromPos(pos, self.ajdList)
                if len(legalMoves) == 0:
                    return False
                # Find pos with least options to be chosen
                if not tryMoves:
                    tryMoves = (pos, legalMoves)
                else:
                    if (len(legalMoves) < len(tryMoves[1])) or (len(legalMoves) == len(tryMoves[1]) and tryMoves[1][0] in self.puzzel.nodes):
                        tryMoves = (pos, legalMoves)

        for pos in tryMoves[1]:
            self.puzzel.connect2Pos(tryMoves[0], pos, self.ajdList)
            if self.backtrackWithHeuristic():
                return True
            self.puzzel.delConnect2Pos(tryMoves[0], pos, self.ajdList)
            self.puzzel.printStateToFile(self.ajdList, "solution.txt")

        return False

    def solve(self):
        with open("solution.txt", "w") as file:
            file.write("Puzzel:\n\n")
        self.puzzel.printStateToFile(self.ajdList, "solution.txt")

        with open("solution.txt", "a") as file:  
            file.write("1. Preprocessing\n\n")
        self.preprocessing()

        with open("solution.txt", "a") as file:  
            file.write("2. Start solving with backtracking\n\n")
        self.backtrackWithHeuristic()
        
        return self.ajdList
    
    
class MasyuDFSSolver:
    def  __init__(self, puzzel: Masyu):
        self.puzzel = puzzel
        self.ajdList: dict[tuple[int, int], list[tuple[int,int]]] = {}
       
    def isEqual(self, ajdList: dict[tuple[int, int], list[tuple[int,int]]]):
        if len(ajdList) != len(self.ajdList):
            return False
        for pos in self.ajdList:
            if pos not in ajdList or len(self.ajdList[pos]) != len(ajdList[pos]):
                return False
            for ajdPos in self.ajdList[pos]:
                if ajdPos not in ajdList[pos]:
                    return False
        return True

    def dfs(self, visited=None):
        
        if self.puzzel.isGoal(self.ajdList):
            return True

        if visited is None:
            visited = []
        visited += [copy.deepcopy(self.ajdList)]
        self.puzzel.printStateToFile(self.ajdList, "solution.txt")

        tryMoves = []
        for i in range(self.puzzel.size):
            for j in range(self.puzzel.size):
                if (i,j) in self.ajdList and len(self.ajdList[(i,j)]) > 1:
                    continue
                legalMoves = self.puzzel.makeLegalConnectsFromPos((i,j), self.ajdList)
                if ((i,j) in self.ajdList or (i,j) in self.puzzel.nodes) and len(legalMoves) == 0:
                    return False
                if (i,j) in self.ajdList or (i,j) in self.puzzel.nodes:
                    tryMoves += [((i,j), legalMoves)]    
                else:
                    tryMoves += [((i,j), tryPos) for tryPos in legalMoves]
        for move in tryMoves:   
            if type(move[1]) is not list:
                self.puzzel.connect2Pos(move[0], move[1], self.ajdList)
                isVisited = False
                for state in visited:
                    if self.isEqual(state):
                        self.puzzel.delConnect2Pos(move[0], move[1], self.ajdList)
                        isVisited = True
                        break
                if not isVisited:
                    if self.dfs(visited):
                        return True
                    self.puzzel.delConnect2Pos(move[0], move[1], self.ajdList)
                    self.puzzel.printStateToFile(self.ajdList, "solution.txt")
            else:
                for pos in move[1]:
                    self.puzzel.connect2Pos(move[0], pos, self.ajdList)
                    isVisited = False
                    for i in range(len(visited)):
                        if self.isEqual(visited[i]):
                            self.puzzel.delConnect2Pos(move[0], pos, self.ajdList)
                            isVisited = True
                            break
                    if not isVisited:
                        if self.dfs(visited):
                            return True
                        self.puzzel.delConnect2Pos(move[0], pos, self.ajdList)
                        self.puzzel.printStateToFile(self.ajdList, "solution.txt")
                return False

        return False

    def solve(self):
        with open("solution.txt", "w") as file:
            file.write("Puzzel:\n\n")
        self.puzzel.printStateToFile(self.ajdList, "solution.txt")

        with open("solution.txt", "a") as file:  
            file.write("Searching with DFS\n\n")
        self.dfs()
        
        return self.ajdList