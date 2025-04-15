#
#
#Jenna Flannery
#
#AI Project 1
#
#Septemeber 17, 2024
#
#This program uses breadth first search and A* search to solve the 8-puzzle problem
#
#


import random
from datetime import datetime
import heapq


def arraySwap(array, i, j):
    #creates new array by swapping specified position in input array
    newArray = array.copy()
    newArray[i],newArray[j] = newArray[j],newArray[i]
    return(newArray)

class State:
    #keeps track of state information
    def __init__(self, posArray, parent, depth):
        self.posArray = posArray
        self.parent = parent
        self.depth = depth

    def __str__(self):
        #print board
        return f"{self.posArray[0]} {self.posArray[1]} {self.posArray[2]}\n{self.posArray[3]} {self.posArray[4]} {self.posArray[5]}\n{self.posArray[6]} {self.posArray[7]} {self.posArray[8]}\n"

    def expand(self):
        #returns children of current node
        #get position of empty space (indicated by 0 in array)
        emptySpace = self.posArray.index(0)
        #check if emptySpace is even or odd
        if emptySpace % 2 == 0:
            if emptySpace == 4:
                #4 possible states(center): swap with pos 1,3,5,7
                child1 = State(arraySwap(self.posArray,emptySpace,1),self,self.depth + 1)
                child2 = State(arraySwap(self.posArray,emptySpace,3),self,self.depth + 1)
                child3 = State(arraySwap(self.posArray,emptySpace,5),self,self.depth + 1)
                child4 = State(arraySwap(self.posArray,emptySpace,7),self,self.depth + 1)
                return child1,child2,child3,child4
            #2 possible states
            elif (emptySpace == 0 or emptySpace == 2):
                #if emptySpace is 0 or 2(upper corners), it swaps with 1 and the pos that is 3 ahead
                child1 = State(arraySwap(self.posArray,emptySpace,1),self,self.depth + 1)
                child2 = State(arraySwap(self.posArray,emptySpace,emptySpace + 3),self,self.depth + 1)
                return child1,child2
            elif (emptySpace == 6 or emptySpace == 8):
                #if emptySpace is 6 or 8(lower corners), it swaps with pos 7 and the pos that is 3 behind
                child1 = State(arraySwap(self.posArray,emptySpace,7),self,self.depth + 1)
                child2 = State(arraySwap(self.posArray,emptySpace,emptySpace - 3),self,self.depth + 1)
                return child1,child2
        else:
            #3 possible states(outside middle): swaps with pos 4
            child1 = State(arraySwap(self.posArray,emptySpace,4),self,self.depth + 1)
            if (emptySpace == 1 or emptySpace == 7):
                #if emptySpace is 1 or 7 (upper and lower middle), it swaps with left and right tile
                child2 = State(arraySwap(self.posArray,emptySpace,emptySpace - 1),self,self.depth + 1)
                child3 = State(arraySwap(self.posArray,emptySpace,emptySpace + 1),self,self.depth + 1)
                return child1,child2,child3
            elif(emptySpace == 5 or emptySpace == 3):
                #if emptySpace is 3 or 5 (left and right middle), it swaps with tile above and below
                child2 = State(arraySwap(self.posArray,emptySpace,emptySpace - 3),self,self.depth + 1)
                child3 = State(arraySwap(self.posArray,emptySpace,emptySpace + 3),self,self.depth + 1)
                return child1,child2,child3


def generateInitial():
    #shuffle array representing goal state to generate intial state
    startArray = [1,2,3,4,5,6,7,8,0]
    random.shuffle(startArray)
    initial = State(startArray,None,0)
    return initial

def breadthFirstSearch(start):
    #stop after 5 seconds
    startTime = datetime.now()
    #define goal:
    goalArray = [1,2,3,4,5,6,7,8,0]
    #generate initial state
    startState = start
    #create fringe (FIFO queue)
    fringe = []
    #create closed list to prevent generating nodes that have already been visited
    closed = []
    #add startState to fringe
    fringe.append(startState)
    #create boolean for goal
    goal = 0
    #pop fringe until goal state is found
    numNodes = 1;
    print("Running Breadth first...")
    while not goal:
        currentTime = datetime.now() - startTime
        if currentTime.total_seconds() >= 10:
            print("program timed out")
            print("Num of nodes: " + str(numNodes))
            return 0
        #print("Current State: ")
        currentState = fringe.pop(0)
        closed.append(currentState.posArray)
        #print(currentState)
        if currentState.posArray == goalArray:
            goal = 1
            print("Goal found at depth: " + str(currentState.depth))
            print("Num of nodes: " + str(numNodes))
            print(currentState)
            return 1
        else:
            #expand current state, check closed list, calculate heuristic, add them to queue
            for j in currentState.expand():
                numNodes += 1;
                if j.posArray not in closed:
                    fringe.append(j)
        
def findSeed():
    #this is a script to find acceptable seeds, not used in main function of program
    #set seed
    #498 1054
    winCount = 0
    startSeed = 1054
    while winCount < 2:
        random.seed(startSeed)
        print("Trying: " + str(startSeed))
        for i in range(3):
            if i == 2 and winCount == 0:
                break
            else:
                winCount += breadthFirstSearch(generateInitial())
        if winCount >= 2:
            print("Seed Found!!!")
            print(startSeed)
            break
        else:
            winCount = 0
            startSeed += 1

def findMismatched(goalArray,targetArray):
    #find the number of misplaced tiles
    misMatched = 0
    for i in range(9):
        if goalArray[i] != targetArray[i]:
            misMatched += 1
    return misMatched

def aStarSearch(start):
    #stop after 10 seconds
    startTime = datetime.now()
    #define goal:
    goalArray = [1,2,3,4,5,6,7,8,0]
    #generate initial state
    startState = start
    #create fringe (Priority queue)(implemented as minheap)
    fringe = []
    #used when nodes are expanded and added to heap, keeps track of order of expansion, so if num mismatched is equal,
    #the node expanded second will be after the node expanded first (also heapq will never try to compare states)
    displace = 0
    #add startState to fringe
    fringe.append((0,0,startState))
    #create closed:
    closed = []
    #create boolean for goal
    goal = 0
    #pop fringe until goal state is found
    numNodes = 1;
    print("Running A*...")
    while not goal:
        currentTime = datetime.now() - startTime
        if currentTime.total_seconds() >= 10:
            print("program timed out")
            print("Num of nodes: " + str(numNodes))
            return 0
        #index is 2 because each node in heap represents tuple: (numMismatched,displace,state)
        currentState = heapq.heappop(fringe)[2]
        closed.append(currentState.posArray)
        if currentState.posArray == goalArray:
            goal = 1
            print("Goal found at depth: " + str(currentState.depth))
            print("Num of nodes: " + str(numNodes))
            print(currentState)
            return 1
        else:
            #expand current state, check closed list, add them to queue
            for j in currentState.expand():
                if j.posArray not in closed:
                    numNodes += 1;
                    m = findMismatched(goalArray,j.posArray)
                    #push node on to heap sorted by num of mismatched tiles + path cost
                    heapq.heappush(fringe,(m+j.depth,displace,j))
                    displace += 1
#testing
random.seed(1054)
print("BEGIN TESTING!!!")
for i in range(3):
    print("*** ROUND " + str(i + 1) + " ***")
    print("Initial State:")
    initialState = generateInitial()
    print(initialState)
    breadthFirstSearch(initialState)
    print("\n")
    aStarSearch(initialState)



