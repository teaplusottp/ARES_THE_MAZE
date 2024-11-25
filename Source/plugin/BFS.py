
from collections import deque
import os
import sys
import time
import tracemalloc

sys.path.append(os.path.dirname(__file__))
import getInput
import support


DIRECTIONS =  {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}

def is_valid(pos, grid):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

def move(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])
def all_boxes_on_goals(box_positions, goals):
    return all(box in goals for box in box_positions)
def bfs_sokoban(grid):
    player_start, boxes, goals = support.parse_grid(grid)
    print(player_start, boxes, goals )
    initial_state = (player_start, tuple(boxes))
    queue = deque([(initial_state, 0,"")])  
    visited = set()
    visited.add(initial_state)
    Node=0
    while queue:
        (player, box_positions), steps,path = queue.popleft()
        if all_boxes_on_goals(box_positions, goals):
            return path, Node 
        for k,direction in DIRECTIONS.items():
            new_player = move(player, direction)
            if is_valid(new_player, grid):
                if new_player in box_positions:
                    new_box = move(new_player, direction) 
                    if is_valid(new_box, grid) and new_box not in box_positions:
                        new_box_positions = tuple(
                            new_box if b == new_player else b for b in box_positions
                        )
                        new_state = (new_player, new_box_positions)
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, steps + 1,path+k.upper()))
                else:
                    new_state = (new_player, box_positions)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, steps + 1,path+k))
                Node+=1
    return "", 0

def BFS(grid,val):
    start = time.time()
    tracemalloc.start()
    res=bfs_sokoban(grid)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    t =  time.time() - start
    stone_data=support.initialize_stones(grid,val)
    p=support.find_object(grid,"+") 
    p=support.find_object(grid,"@") if p is None else p 
    if(res[1]==0):
        w=0
    else:
        w=support.findWeight(res[0],stone_data,p)
    return "Steps: " + str(len(res[0])) +", Weight: " + str(w) +", Node: " + str(res[1]) +", Time (ms): " + f"{t * 1000:.2f}" +", Memory (MB): " + f"{peak / (1024 * 1024):.2f}\n{res[0]}"

lst_maze = getInput.get_input()
result = BFS(*lst_maze[6])

print(f"Số bước cần thiết: {result}")
