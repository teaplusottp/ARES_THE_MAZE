
# from collections import deque
# import os
# import sys
# import time
# import tracemalloc

# sys.path.append(os.path.dirname(__file__))
# import getInput
# import support


# DIRECTIONS =  {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}

# def is_valid(pos, grid):
#     x, y = pos
#     return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'
# def findWeight(path, stone_data, player):
#     res = 0
#     for step in path:
#         player = tuple(map(sum, zip(player, DIRECTIONS[step.lower()])))
#         if step == step.lower():
#             res += 1
#         elif player in stone_data:
#             res += int(stone_data[player])
#             stone_data[tuple(map(sum, zip(player, DIRECTIONS[step.lower()])))] = stone_data.pop(player)
#     return res
# def move(pos, direction):
#     return (pos[0] + direction[0], pos[1] + direction[1])
# def all_boxes_on_goals(box_positions, goals):
#     return all(box in goals for box in box_positions)
# def initialize_stones(maze, val):
#     stone_data = {}
#     for index, (row, col) in enumerate(((r, c) for r in range(len(maze)) for c in range(len(maze[0])) if(maze[r][c] in ('$','*')))):
#         stone_data[(row, col)] = val[index]
#     return stone_data
# def dfs_sokoban(grid):
#     player_start, boxes, goals = support.parse_grid(grid)
#     initial_state = (player_start, tuple(boxes))
#     queue = deque([(initial_state, 0,"")])  
#     visited = set()
#     visited.add(initial_state)
#     Node=0
#     while queue:
#         (player, box_positions), steps,path = queue.pop()
#         if all_boxes_on_goals(box_positions, goals):
#             return path, Node 
#         for k,direction in DIRECTIONS.items():
#             new_player = move(player, direction)
#             if is_valid(new_player, grid):
#                 if new_player in box_positions:
#                     new_box = move(new_player, direction) 
#                     if is_valid(new_box, grid) and new_box not in box_positions:
#                         new_box_positions = tuple(
#                             new_box if b == new_player else b for b in box_positions
#                         )
#                         new_state = (new_player, new_box_positions)
#                         if new_state not in visited:
#                             visited.add(new_state)
#                             queue.append((new_state, steps + 1,path+k.upper()))
#                 else:
#                     new_state = (new_player, box_positions)
#                     if new_state not in visited:
#                         visited.add(new_state)
#                         queue.append((new_state, steps + 1,path+k))
#                 Node+=1
#     return ",",-1  

# def DFS(grid,val):
#     start = time.time()
#     tracemalloc.start()
#     res=dfs_sokoban(grid)
#     peak = tracemalloc.get_traced_memory()[1]
#     tracemalloc.stop()
#     t =  time.time() - start
#     stone_data=initialize_stones(grid,val)
#     p=support.find_object(grid,"+") 
#     p=support.find_object(grid,"@") if p is None else p 
#     w=findWeight(res[0],stone_data,p)
#     return "Steps: " + str(len(res[0])) +", Weight: " + str(w) +", Node: " + str(res[1]) +", Time (ms): " + f"{t * 1000:.2f}" +", Memory (MB): " + f"{peak / (1024 * 1024):.2f}\n{res[0]}"

from datetime import datetime
import time
import tracemalloc
import support
import sys
import os
from collections import deque

sys.path.append(os.path.dirname(__file__))
import getInput

DIRECTIONS = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}


def move(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])

def all_stones_on_targets(stone_positions, targets):
    return all(stone in targets for stone in stone_positions)

def is_valid(pos, maze):
    x, y = pos
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != '#'

def dfs(maze):
    player_start, stones, targets = support.parse_grid(maze)
    initial_state = (player_start, tuple(stones))
    stack = [(initial_state, 0, "")]  
    visited = set()
    visited.add(initial_state)
    node = 0

    while stack:
        (player, box_positions), steps, path = stack.pop(-1)
        if all_stones_on_targets(box_positions, targets):
            return path, node 
        for k, direction in DIRECTIONS.items():
            new_player = move(player, direction)
            if is_valid(new_player, maze):
                if new_player in box_positions:
                    new_box = move(new_player, direction) 
                    if is_valid(new_box, maze) and new_box not in box_positions:
                        new_box_positions = tuple(
                            new_box if b == new_player else b for b in box_positions
                        )
                        new_state = (new_player, new_box_positions)
                        if new_state not in visited:
                            visited.add(new_state)
                            stack.append((new_state, steps + 1,path+k.upper()))
                else:
                    new_state = (new_player, box_positions)
                    if new_state not in visited:
                        visited.add(new_state)
                        stack.append((new_state, steps + 1,path+k))
                node += 1
    return "", 0

def DFS(maze,val):
    start = time.time()
    tracemalloc.start()
    res = dfs(maze)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    t = time.time() - start
    stone_data=support.initialize_stones(maze,val)
    p = support.find_object(maze,"+") 
    p = support.find_object(maze,"@") if p is None else p 
    if(res[1]==0):
        w=0
    else:
        w=support.findWeight(res[0],stone_data,p)
    return "Steps: " + str(len(res[0])) +", Weight: " + str(w) +", Node: " + str(res[1]) +", Time (ms): " + f"{t * 1000:.2f}" +", Memory (MB): " + f"{peak / (1024 * 1024):.2f}\n{res[0]}"

# # Gọi hàm giải maze
# lst_maze=getInput.get_input()
# print(DFS(*lst_maze[1]))
# # print(lst_maze[0])
