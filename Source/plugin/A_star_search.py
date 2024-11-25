import heapq
import time
import tracemalloc
from dataclasses import dataclass
from typing import List, Tuple
import support
import sys
import os

sys.path.append(os.path.dirname(__file__))

# Định nghĩa hướng đi trong mê cung
DIRECTIONS = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}

# Định nghĩa cấu trúc Stone
@dataclass
class Stone:
    position: Tuple[int, int]
    weight: int

# Khởi tạo danh sách các hòn đá và trọng số tương ứng
def initialize_stones(maze, val) -> List[Stone]:
    stones = []
    for index, (row, col) in enumerate(((r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] in ('$','*'))):
        stones.append(Stone(position=(row, col), weight=int(val[index])))
    return stones

# Hàm heuristic
def heuristic(stone_positions, targets):
    return sum(min(int((abs(stone[0] - target[0])**2 + abs(stone[1] - target[1])**2)**0.5+1) for target in targets) for stone in stone_positions)

# Hàm A* để tìm đường đi
def a_star(player, stones, targets, maze, stone_data, max_nodes=1000000000, max_time=100000000):
    queue = [(0, player, tuple(stone.position for stone in stones), "", 0)]
    visited = set([(player, tuple(stone.position for stone in stones))])
    node_count = 0
    start_time = time.time()
    
    while queue:
        if time.time() - start_time > max_time:
            print("Exceeded time limit")
            return "", 0, 0, 0 
        if node_count > max_nodes:
            print("Exceeded node expansion limit")
            return "", 0, 0, 0 
        
        current_cost, player_pos, stone_positions, path, total_weight = heapq.heappop(queue)
        
        # Kiểm tra nếu tất cả các viên đá đã vào vị trí đích
        if set(stone_positions) == set(targets):
            return path, node_count, current_cost, total_weight
        
        for direction, move in DIRECTIONS.items():
            new_player_pos = tuple(map(sum, zip(player_pos, move)))
            
            # Kiểm tra tính hợp lệ của vị trí mới
            if not support.valid_position(maze, new_player_pos):
                continue
            
            new_stone_positions = list(stone_positions)
            push = False
            move_cost = 1
            new_weight = total_weight
            
            if new_player_pos in stone_positions:
                stone_index = stone_positions.index(new_player_pos)
                new_stone_pos = tuple(map(sum, zip(new_player_pos, move)))
                
                # Kiểm tra tính hợp lệ khi di chuyển viên đá
                if not support.valid_position(maze, new_stone_pos) or new_stone_pos in stone_positions:
                    continue
                
                # Cập nhật vị trí mới cho viên đá
                push = True
                move_cost += stones[stone_index].weight
                new_weight += stones[stone_index].weight
                new_stone_positions[stone_index] = new_stone_pos

            new_state = (new_player_pos, tuple(new_stone_positions))
            
            if new_state not in visited:
                visited.add(new_state)
                heuristic_cost = heuristic(new_stone_positions, targets)
                total_cost = current_cost + move_cost + heuristic_cost
                new_path = path + direction.upper() if push else path + direction
                heapq.heappush(queue, (total_cost, new_player_pos, tuple(new_stone_positions), new_path, new_weight))
                node_count += 1
                
    return "", 0, 0, 0   

def A_star(maze, val, output_file=None, max_nodes=10000000, max_time=1000):
    """Giải bài toán mê cung bằng A* Search."""

    stone_data = initialize_stones(maze, val)
    player_pos = support.find_object(maze, "+") 
    player_pos = support.find_object(maze, "@") if player_pos is None else player_pos
    stone_positions = tuple(stone.position for stone in stone_data)
    target_positions = set(support.find_all_objects(maze, ".") + support.find_all_objects(maze, "*") + support.find_all_objects(maze, "+"))

    start_time = time.time()
    tracemalloc.start()
    result = a_star(player_pos, stone_data, target_positions, maze, stone_data, max_nodes, max_time)
    peak_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    end_time = time.time()
    total_time = (end_time - start_time) * 1000  
    total_memory = peak_memory / (1024 * 1024) 
    path, nodes_expanded, total_cost, total_weight = result
    
    result_str = (
        f"Steps: {len(path)}, Weight: {total_weight}, Nodes: {nodes_expanded}, "
        f"Time (ms): {total_time:.2f}, Memory (MB): {total_memory:.2f}\n{path}"
    )
    
    return result_str
