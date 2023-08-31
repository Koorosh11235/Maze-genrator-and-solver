import tkinter as tk 
import numpy as np

maze = [
    [0, 1, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0]
]

def gui(maze):
    window = tk.Tk()
    window.config(bg = "gray")
    window.geometry(f"{len(maze[0])*50}x{len(maze)*50}")
    solve = tk.Button(text="solve", bg = "indian red", command = lambda : solve_gui(maze, window))
    solve.place(x = len(maze[0])*10,y = len(maze)*40+20)
    for a in range(len(maze[0])):
        for b in range(len(maze)):
            if maze[b][a] == 0:
                color  = "white"
            else:
                color = "black"
            temp = tk.Entry(window,justify= "center", bg = color,font = "Areal 20 bold", fg = color)
            temp.place(x=a*40, y=b*40, width=40, height=40)

    window.mainloop()

def solve_gui(maze, window):
    path = solve_maze(maze)
    if path is None:
        label = tk.Label(text = "no\nsolution", bg = "yellow", fg = "green", font="Areal 20 bold")
        label.place(x = len(maze[0])/2*40-60,y = len(maze)/2*40-60, height=120, width=120)
        return

    for a in range(len(maze[0])):
        for b in range(len(maze)):
            if (b,a) in path:
                color  = "slate blue"
            elif maze[b][a] == 0:
                color  = "white"
            else:
                color = "black"
            temp = tk.Entry(window,justify= "center", bg = color,font = "Areal 20 bold", fg = color)
            temp.place(x=a*40, y=b*40, width=40, height=40)
    window.mainloop()

def solve_maze(maze):
    rows, cols= len(maze), len(maze[0])
    start, end = (0,0), (rows-1, cols-1)
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
                if n not in visited and maze[row_n][col_n]==0 :
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
        
    
gui(np.transpose(maze))