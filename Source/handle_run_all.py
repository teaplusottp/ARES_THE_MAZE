import os
from plugin.BFS import BFS
from plugin.DFS import DFS
from plugin.UCS import UCS
from plugin.A_star_search import A_star
from plugin.support import append_to_file,read_path_from_file
from plugin.Var import lst_maze

# Đường dẫn thư mục chứa các file output
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
print("Output directory:", OUTPUT_DIR)

def run_all_algorithms():

    # Danh sách các thuật toán và tên của chúng
    algorithms = [
        (BFS, "BFS"),
        (DFS, "DFS"),
        (UCS, "UCS"),
        (A_star, "A*")
    ]

    for index, (maze, val) in enumerate(lst_maze):
        if (index == 3):
            output_filename = os.path.join(OUTPUT_DIR, f"output-{index+1:02d}.txt")
            for algorithm, name in algorithms:
                if read_path_from_file(name,output_filename) is not None:
                    continue
                result = algorithm(maze, val)
                append_to_file(result, name, output_filename)
                print(f"Đã xử lý {name} cho input-{index+1:02d}")
                print(result)
         
run_all_algorithms()
