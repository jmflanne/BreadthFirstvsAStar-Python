# BreadthFirstvsAStar-Python
The 8-puzzle problem involves a 3x3 grid with 8 numbered tiles and one empty space. The goal is to slide tiles into the empty space until the goal configuration is acheived. In this case, the goal configuration is the tiles placed in increasing order with the empty space in the bottom right corner, or: </br>
1 2 3 </br>
4 5 6 </br>
7 8   </br>

This project builds a tree with each node representing a configuration of the board. The starting node is a random configuration. Two search algorithms are used to find the final configuration: breadth first search and A*. </br>
The A* algorithm uses the number of misplaced tiles as a heuristic function. </br>
Three random start states are used. If an algorithm cannot find the goal state within 10 seconds, the program moves on (either to the A* algorithm using the same initial state or the breadth first search algorithm using a new initial state). </br>
The results show the depth at which the goal state was found and how many nodes were traversed before finding the goal state. </br>

There is also a report attached that compares the performance of the algorithms. 
