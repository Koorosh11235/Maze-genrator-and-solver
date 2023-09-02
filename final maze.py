import tkinter as tk 
import numpy as np
import random

class Maze:
    def __init__(self, height, width, classic = True, method = "recursive") -> None:
        self.height = height
        self.width = width
        self.classic = classic
        self.gui = tk.Tk()
        if method == "recursive":
            self.maze, self.start, self.end = self.generate_maze()
        elif method == "stack" :
            self.maze ,self.start, self.end= self.generate_maze_stack()
        else:
            return

    def generate_maze(self):
        maze = [[1] * self.width for _ in range(self.height)]
        if self.classic :
            start = (0,0)
            goal = (self.height-1, self.width-1)
        else :
            start = (random.randint(0,self.height-1), random.randint(0,self.width-1))
            goal = (random.randint(0,self.height-1), random.randint(0,self.width-1))

        def create_maze(row, col):
            maze[row][col] = 0  # Mark current cell as visited

            # Define the four possible directions (up, down, left, right)
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                n_row, n_col = row + dx, col + dy

                # Check if the neighbor is within the maze boundaries
                if 0 <= n_row < self.height and 0 <= n_col < self.width and maze[n_row][n_col] == 1:
                    # Remove the wall between the current cell and the chosen neighbor
                    maze[row + dx // 2][col + dy // 2] = 0
                    create_maze(n_row, n_col)  # Recursively visit the chosen neighbor

        row, col = start
        rn, coln = goal

        create_maze(row, col)  # Start generating the maze from the top-left cell
        maze[rn][coln] = 0
        if self.classic :
            if maze[rn][coln-1] and maze[rn-1][coln]:
                maze[rn][coln-1], maze[rn-1][coln] = 0 ,0

        return maze, start, goal
            
    def generate_maze_stack(self):
        # Initialize maze with all walls
        maze = [[1] * self.width for _ in range(self.height)]
        if self.classic:
            start = (0,0)
            goal = (self.height-1,self.self.width-1)
        else:
            start = (random.randint(0,self.height-1), random.randint(0,self.width-1))
            goal = (random.randint(0,self.height-1), random.randint(0,self.width-1))

        stack = [start]  # Start with the top-left cell
        visited = set([start])  # Mark the top-left cell as visited
        while stack:
        # Initialize maze with all walls
            """ In the provided code, the algorithm assumes that all cells are 
            initially walls and then removes walls to create passages. Therefore,
            by selecting an unvisited neighboring cell, the algorithm guarantees
            that the chosen neighbor cell is walkable because it has already
            removed the wall between the current cell and the chosen neighbor."""
            row, col = stack.pop()
            maze[row][col] = 0  # Mark current cell as visited

            # Define the four possible directions (up, down, left, right)
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                n_row, n_col = row + dx, col + dy

                # Check if the neighbor is within the maze boundaries
                if 0 <= n_row < self.height and 0 <= n_col < self.width and (n_row, n_col) not in visited:
                    # Remove the wall between the current cell and the chosen neighbor
                    maze[row + dx // 2][col + dy // 2] = 0
                    stack.append((n_row, n_col))  # Add the chosen neighbor to the stack
                    visited.add((n_row, n_col))  # Mark the chosen neighbor as visited

        maze[goal[0]][goal[1]] = 0  # Mark the bottom-right cell as open
        if maze[goal[0]-1][goal[1]] == 1 and maze[goal[0]+1][goal[1]]==1 :
        # Mark the bottom-right cell as open
            if maze[goal[0]][goal[1]-1] ==1 and maze[goal[0]][goal[1]+1] == 1 :
                maze[goal[0]-1][goal[1]] = 0  # Mark the bottom-right cell as open
                maze[goal[0]+1][goal[1]] = 0  # Mark the bottom-right cell as open
                maze[goal[0]][goal[1]-1] = 0  # Mark the bottom-right cell as open
                maze[goal[0]][goal[1]+1] = 0  # Mark the bottom-right cell as open

        return maze, start, goal
    

    def make_gui(self):
        self.gui.config(bg = "gray")
        self.gui.geometry(f"{len(self.maze[0])*35}x{len(self.maze)*35}")
        solve = tk.Button(text="solve", bg = "magenta", command = self.solve_gui)
        solve.place(x = len(self.maze[0])*10,y = len(self.maze)*30+20)
        for a in range(len(self.maze[0])):
            for b in range(len(self.maze)):
                if self.maze[b][a] == 0:
                    color  = "white"
                else:
                    color = "black"
                temp = tk.Entry(self.gui,justify= "center", bg = color,font = "Areal 20 bold", fg = color)
                temp.place(x=a*30, y=b*30, width=30, height=30)
                if (b,a) == self.start:
                    temp.insert(15, "S")
                    temp.config(fg = "red")
                if (b,a) == self.end:
                    temp.insert(15, "G")
                    temp.config(fg = "red")

        self.gui.mainloop()
        
    def solve_gui(self):
        path = self.solve_maze()
        if path is None:
            label = tk.Label(text = "no\nsolution", bg = "yellow", fg = "green", font="Areal 20 bold")
            label.place(x = len(self.maze[0])/2*30-60,y = len(self.maze)/2*30-60, height=120, width=120)
            return

        for a in range(len(self.maze[0])):
            for b in range(len(self.maze)):
                if (b,a) in path:
                    color  = "slate blue"
                elif self.maze[b][a] == 0:
                    color  = "white"
                else:
                    color = "black"
                temp = tk.Entry(self.gui,justify= "center", bg = color,font = "Areal 20 bold", fg = color)
                temp.place(x=a*30, y=b*30, width=30, height=30)
                if (b,a) == self.start:
                    temp.insert(15, "S")
                    temp.config(fg = "red")
                if (b,a) == self.end:
                    temp.insert(15, "G")
                    temp.config(fg = "red")

        self.gui.mainloop()

    def solve_maze(self ):
        rows, cols= len(self.maze), len(self.maze[0])
        start, end = self.start, self.end
        stack = [start]
        visited= []
        parnets = {}

        while stack:
            current = stack.pop()
            row , col  = current
            
            if current == end :
                break
            
            neighbours = [
                (row+1, col),
                (row-1, col),
                (row, col+1),
                (row, col-1),
            ]

            for n in neighbours :
                row_n, col_n = n
                if 0<=row_n<rows and 0<=col_n<cols:
                    if n not in visited and self.maze[row_n][col_n]==0 :
                        stack.append(n)
                        visited.append(n)
                        parnets[n] = current

        if end in parnets:
            path = []
            while current != start:
                path.append(current)
                current = parnets[current]
            path.append(start)
            path.reverse()
            return path
maze = Maze(22 , 33)
#maze = Maze(height=20, width=36, classic=True, method="recursive") default
#maze = Maze(height=21, width=35, classic= False , method="stack")
maze.make_gui()


