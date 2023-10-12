"""
    Exercise for Artificial Intelligence class.

    State search problem.

    Base repo url: https://github.com/rcpsilva/BCC325_ArtificialIntelligence/tree/main/2023-2/SourceCode
"""


import numpy as np
import matplotlib.pyplot as plt

# Stack implementation
from collections import deque

class Maze():

    def __init__(self,nrow,ncol,start,exit,pobs=.3,pause=1):

        self.map = np.zeros((nrow,ncol))
        self.start = np.array(start)
        self.exit = np.array(exit)

        #add obstacles

        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if np.random.rand() < pobs and ([i,j]!=self.start).any() and ([i,j]!=self.exit).any():
                    self.map[i][j] = 1

        ################## visualization ###################
        self.map[start[0]][start[1]] = 0.8 
        self.map[exit[0]][exit[1]] = 0.3
        self.pause = pause
        plt.ion()
        self.vis_map()
        plt.draw()
        plt.pause(pause)
        plt.clf()
        ###################################################
                   
    def initial_percepts(self):

        return {'pos':self.start,
                'exit':self.exit,
                'neighbors':self.get_neighbors(self.start),
                'path':[]}
    
    def get_neighbors(self,pos):

        directions = np.array([[1,0],[-1,0],[0,1],[0,-1]])
        candidates = [pos + dir for dir in directions]
        neighbors = [c for c in candidates if (c[0]>=0 and c[0]<self.map.shape[0]) and (c[1]>=0 and c[1]<self.map.shape[1]) and (self.map[c[0]][c[1]] !=1)]

        return neighbors
    
    def state_transition(self,action):

        ################## visualization ###################
        plt.ion()
        self.plot_path(action['path'],self.pause)
        ####################################################

        return {'pos': action['move_to'],
                'exit':self.exit,
                'neighbors':self.get_neighbors(action['move_to']),
                'path':action['path']}
    
    # Visualization functions ###############################
    def plot_path(self, path, pause_time):
        plt.axes().invert_yaxis()
        plt.pcolormesh(self.map)
        for i in range(len(path)-1):
            plt.plot([path[i][1]+0.5,path[i+1][1]+0.5],[path[i][0]+0.5,path[i+1][0]+0.5],'-rs')
        plt.draw()
        plt.pause(pause_time)
        plt.clf()

    def vis_map(self):
        plt.axes().invert_yaxis()
        plt.pcolormesh(self.map)
        plt.plot(self.start[1]+0.5, self.start[0]+0.5,'rs')
        plt.show()
    ##########################################################

def create_action(move_to, path=[]):
    return {'move_to':move_to,
            'path':path}

def recreate_path(path_memory, final_vertice):
    path = []
    v = final_vertice
    while np.any((path_memory[v[0]][v[1]] != [-1, -1])):
        path.append(v)
        v = path_memory[v[0]][v[1]]
    path.append(v)
    return path[::-1]

def main_dfs():
    # Environment setup
    nrow = 5
    ncol = 5
    env = Maze(nrow,ncol,[0,0],[nrow-1,ncol-1], pobs=.3)

    initial_percepts = env.initial_percepts()
    objective = initial_percepts['exit']
    start_point = initial_percepts['pos']

    # Auxiliar variables for dfs and path tracing
    stack = deque()
    discovered = [[False for _ in range(ncol)] for _ in range(nrow)]
    path_memory = [[[-1, -1] for _ in range(ncol)] for _ in range(nrow)]
    stack.append(start_point)
    
    found_solution = False
    while len(stack) != 0:
        v = stack.pop()
        if not discovered[v[0]][v[1]]:

            discovered[v[0]][v[1]] = True

            # Found the exit
            if v[0] == objective[0] and v[1] == objective[1]:
                path = recreate_path(path_memory, v)
                print("Solution was found!")
                print("Path = ", path)
                print("Closing in 5 seconds...")

                env.plot_path(path, 5)
                found_solution = True
                break
            
            # Exit not found -> next transition
            percepts = env.state_transition(create_action(v, recreate_path(path_memory, v)))
            for vertice in percepts['neighbors']:
                if not discovered[vertice[0]][vertice[1]]:
                    path_memory[vertice[0]][vertice[1]] = v # The arbitrary vertice w recognizes v as it's "father"
                stack.append(vertice)

    if not found_solution:
        print("Solution does not exist!")

def main_bfs():
    # Environment setup
    nrow = 5
    ncol = 5
    env = Maze(nrow,ncol,[0,0],[nrow-1,ncol-1], pobs=.3)

    initial_percepts = env.initial_percepts()
    objective = initial_percepts['exit']
    start_point = initial_percepts['pos']

    # Auxiliar variables for bfs and path tracing
    queue = deque()
    discovered = [[-1 for _ in range(ncol)] for _ in range(nrow)]
    path_memory = [[[-1, -1] for _ in range(ncol)] for _ in range(nrow)]
    queue.append(start_point)
    
    found_solution = False
    while len(queue) != 0:
        v = queue.popleft()
        if -1<=discovered[v[0]][v[1]]<=0:

            discovered[v[0]][v[1]] = 1

            # Found the exit
            if v[0] == objective[0] and v[1] == objective[1]:
                path = recreate_path(path_memory, v)
                print("Solution was found!")
                print("Path = ", path)
                print("Closing in 5 seconds...")

                env.plot_path(path, 5)
                found_solution = True
                break
            
            # Exit not found -> next transition
            percepts = env.state_transition(create_action(v, recreate_path(path_memory, v)))
            for vertice in percepts['neighbors']:
                if discovered[vertice[0]][vertice[1]] == -1:
                    path_memory[vertice[0]][vertice[1]] = v # The arbitrary vertice w recognizes v as it's "father"
                    discovered[vertice[0]][vertice[1]] = 0
                queue.append(vertice)

    if not found_solution:
        print("Solution does not exist!")

if __name__ == '__main__':

    print("Agent configured with DFS algorithm:")
    main_dfs()

    print("\n\nAgent configured with BFS algorithm:")
    main_bfs()