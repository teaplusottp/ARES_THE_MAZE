import sys

# Giới hạn độ sâu đệ quy nếu muốn dùng cách này
sys.setrecursionlimit(2000)

# Kích thước mê cung
N = 6  # Số dòng
M = 6  # Số cột

# Danh sách các tường trong mê cung (đường ngang và dọc)
walls = [
    (1, 2, 3, 2),  # Tường dọc từ (1,2) đến (3,2)
    (0, 4, 3, 4),  # Tường dọc từ (0,4) đến (3,4)
    (1, 1, 1, 3),  # Tường ngang từ (1,1) đến (1,3)
    (2, 3, 2, 5),  # Tường ngang từ (2,3) đến (2,5)
]

# Các hướng di chuyển
DIRECTIONS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}

# Kiểm tra va chạm với tường
def hit_wall(x, y, nx, ny):
    for (x1, y1, x2, y2) in walls:
        if x == x1 == x2 and min(y, ny) < y1 < max(y, ny):
            return True
        if y == y1 == y2 and min(x, nx) < x1 < max(x, nx):
            return True
    return False

# Hàm duyệt mê cung dùng stack thay vì đệ quy
def find_paths(start_x, start_y, max_velocity):
    stack = [(start_x, start_y, None, 1, [(start_x, start_y, None, 1)])]
    total_paths = 0
    
    while stack:
        x, y, direction, velocity, path = stack.pop()
        
        if (x, y) == (0, 0):
            print("Tìm thấy lối thoát:", path)
            total_paths += 1
            continue
        
        for d, (dx, dy) in DIRECTIONS.items():
            if direction and (d == opposite(direction)):
                continue
            
            nx, ny = x + velocity * dx, y + velocity * dy
            if 0 <= nx < N and 0 <= ny < M and not hit_wall(x, y, nx, ny):
                new_path = path + [(nx, ny, d, velocity)]
                stack.append((nx, ny, d, velocity, new_path))
        
        if velocity > 1:
            stack.append((x, y, direction, velocity - 1, path))
        elif velocity < max_velocity:
            stack.append((x, y, direction, velocity + 1, path))
    
    return total_paths

def opposite(direction):
    opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
    return opposites[direction]

# Khởi chạy tìm kiếm
initial_position = (5, 0)  # Vị trí ban đầu
max_velocity = 3  # Giới hạn vận tốc
total_paths = find_paths(initial_position[0], initial_position[1], max_velocity)

print("Tổng số đường đi hợp lệ:", total_paths)
