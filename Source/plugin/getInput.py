import os
import numpy as np

WINDOWN_BLOCK_SHAPE = (15, 25)

def get_file_names():
    target_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  
    files = [ os.path.join(target_dir, f)  for f in os.listdir(target_dir) if f.startswith('input-') and f.endswith('.txt')]
    return files

def check_first(lst):
    for j in range(len(lst)):
        if(lst[j]=="#" ):
            return lst
        lst[j]=lst[j].replace(" ","")
    return lst
def check_maze(maze):
    rows, cols = len(maze), len(maze[0])
    for col in range(cols):
        found_block_down = False  
        found_block_up = False  
        for row in range(rows):
            if maze[row][col] == '#':
                found_block_up = True
            elif not found_block_up and maze[row][col] == ' ':
                maze[row][col] = ''
            if maze[rows - 1 - row][col] == '#':
                found_block_down = True
            elif not found_block_down and maze[rows - 1 - row][col] == ' ':
                maze[rows - 1 - row][col] = ''
    for row in range(rows):
        found_block = False  
        for col in range(cols):
            if maze[row][col] == '#':
                found_block = True
            elif not found_block and maze[row][col] == ' ':
                maze[row][col] = ''

    return maze
def check_first_vertical(maze):
    rows, cols = len(maze), len(maze[0])
    for col in range(cols):
        found_block = False 
        for row in range(rows):
            if maze[row][col] == '#':
                found_block = True  
            elif not found_block and maze[row][col] == ' ':
                maze[row][col] = ''
    return maze
def convert_to_maze(s):
    lines = s.strip().split('\n')
    val = lines[0].split()
    maze = [list(line) for line in lines[1:]]
    formal_maze = np.full(WINDOWN_BLOCK_SHAPE, "", dtype=object)
    for i in range(len(maze)):
        formal_maze[i + 1, 1:len(maze[i]) + 1] = check_first(maze[i])
    return check_maze(formal_maze), val

def get_input():
    input_files = get_file_names()
    res=[]
    for name in input_files:
        with open(name, "r") as f:
            s = f.read()
            res.append(convert_to_maze(s))
    return res



def delete_output_files():
    # Lấy thư mục chứa file hiện tại
    target_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Lấy danh sách tất cả các file trong thư mục
    files = os.listdir(target_dir)

    # Duyệt qua tất cả các file và xóa file nào bắt đầu bằng 'output-' và kết thúc bằng '.txt'
    for file in files:
        if file.startswith('output-') and file.endswith('.txt'):
            file_path = os.path.join(target_dir, file)
            os.remove(file_path)  # Xóa file
            print(f"Deleted: {file_path}")  # In ra thông báo đã xóa
