import sys
import os
sys.path.append(os.path.dirname(__file__))
import getInput

lst_maze = getInput.get_input()  

DIRECTIONS = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
