import os
import sys

sys.path.append(os.path.dirname(__file__))
from Var import DIRECTIONS

def images_are_equal(img1, img2):
    if img1.get_size() != img2.get_size():
        return False
    for x in range(img1.get_width()):
        for y in range(img1.get_height()):
            if img1.get_at((x, y)) != img2.get_at((x, y)):
                return False
    return True

def find_object(maze,obj):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == obj:
                return (row, col)
    return None

def find_all_objects(maze, obj):
    positions = []
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == obj:
                positions.append((i, j))
    return positions

def parse_maze_with_weights(maze, weights):
    stones = []
    weight_index = 0
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == "$":
                stones.append(((i, j), weights[weight_index]))
                weight_index += 1
    return stones

def valid_position(maze, pos):
    x, y = pos
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != "#"



def initialize_stones(maze, val):
    stone_data = {}
    for index, (row, col) in enumerate(((r, c) for r in range(len(maze)) for c in range(len(maze[0])) if(maze[r][c] in ('$','*')))):
        stone_data[(row, col)] = val[index]
    return stone_data


def append_to_file(data, method, filename):
    with open(filename, 'a') as file:
        file.write(f"{method}\n")
        file.write(data + '\n')

def read_path_from_file(method, filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' không tồn tại.")
        return None
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines += "\n"
    for i in range(len(lines)):
        if lines[i].strip() == method:
            path_line = lines[i+2].strip()
            return path_line    
    return None
def is_ket(stone,maze):
    DIRECTIONS = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    res=""
    for k,v in DIRECTIONS.items():
        tmp=tuple(map(sum,zip(stone,v)))
        if(maze[tmp]=="#"):
            res+=k
    if(len(res)==1):
        return False
    is_ket_lst=['ul','ur','dl','dr']
    for j in is_ket_lst:
        if(j in res):
            return True
    return False

def ket_goc(maze,stone_pos):
    for i in stone_pos:
        if(is_ket(i,maze)):
            return True
    return False

def parse_grid(grid):
    player_start = None
    boxes = []
    goals = []

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '$':
                boxes.append((i, j))
            elif cell == '.': 
                goals.append((i, j))
            elif cell == '*': 
                boxes.append((i, j))
                goals.append((i, j))
            elif cell == '+': 
                player_start = (i, j)
                goals.append((i, j))
            elif cell == '@': 
                player_start = (i, j)
    return player_start, boxes, goals


def findWeight(path, stone_data, player):
    res = 0
    for step in path:
        player = tuple(map(sum, zip(player, DIRECTIONS[step.lower()])))
        if player in stone_data:
            res += int(stone_data[player])
            stone_data[tuple(map(sum, zip(player, DIRECTIONS[step.lower()])))] = stone_data.pop(player)
    return res
def findWeightNDisplay(path, stone, player):
    res_lst=[]
    res = 0
    stone_data=stone.copy()
    for step in path:
        player = tuple(map(sum, zip(player, DIRECTIONS[step.lower()])))
        if step == step.lower():
            res += 0
        elif player in stone_data:
            res += int(stone_data[player])
            stone_data[tuple(map(sum, zip(player, DIRECTIONS[step.lower()])))] = stone_data.pop(player)
        res_lst.append(res)
    return res_lst