import pygame
import sys
import copy
from datetime import datetime
import os

# from plugin.loading import Loading
from plugin import support
# from plugin.getInput import get_input
# from plugin.getInput import delete_output_files
from plugin.button import Button

from plugin.Var import lst_maze
from plugin.BFS import BFS
from plugin.DFS import DFS
from plugin.UCS import UCS
from plugin.A_star_search import A_star

from plugin.support import find_object
from plugin.Fade import Fade

# Constants
TILE_SIZE = 40
ROWS, COLS = 15, 25
SIDEBAR_WIDTH, DOWBAR_HEIGHT = 200, 100
WINDOW_WIDTH = SIDEBAR_WIDTH + TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS + DOWBAR_HEIGHT
MOVE_INTERVAL = 200  # ms between moves
BUTTON_HEIGHT = 50

# Colors
GRAY_IN, GRAY_OUT = (200, 200, 200), (100, 100, 100)
BLACK, WHITE, GRAY_LINE = (0, 0, 0), (255, 255, 255), (122, 122, 122)
RED = (255, 45, 0)

class Game:
    def __init__(self):
       # delete_output_files()
        pygame.init()
        self.paused = False 
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Special Maze")

        self.font = pygame.font.Font('./resources/font/Minecraft.ttf', 29)
        self.font_in_game = pygame.font.Font('./resources/font/VCR_OSD_MONO_1.001.ttf', 14)

        self.maze, self.val = copy.deepcopy(lst_maze[0])
        self.current=0
        self.maze_original = self.maze.copy()
        tmp= find_object(self.maze, "@")
        self.player_pos = tmp if tmp!=None else find_object(self.maze, "+")

        self.stone_data = {}
        self.scroll_offset = 0
        self.last_move_time = datetime.now()
        self.solve=[BFS,DFS,UCS,A_star]
        self.name_alg=["BFS","DFS","UCS","A*"]

        self.moving = False
        self.is_handle=False

        self.load_images()
        self.step=0
        self.weight=0
        
        self.chosen_algorithm = None

        self.initialize_stones()
        #self.handle_algorithm()


    def load_images(self):
        self.bnt_restart = pygame.image.load("./resources/img/restart_bnt.jpg").convert_alpha()
        #self.bnt_restart = pygame.transform.scale(self.bnt_restart, (331, 127))
        self.bnt_img_sub1 = pygame.image.load("./resources/img/wood_texture.jpg").convert_alpha()
        self.bnt_img_sub1 = pygame.transform.scale(self.bnt_img_sub1, (331, 67))
        self.stone_img = self.load_image("./resources/img/Stone.png")
        self.stone_img_2 = self.load_image("./resources/img/Stone_2.png")
        self.man_img = self.load_image("./resources/img/man.png")

        self.man_img_2 = self.load_image("./resources/img/man.png")

        self.target_img = self.load_image("./resources/img/goal.png")
        self.block_img = self.load_image("./resources/img/block.png")
        self.btn_img = pygame.image.load("./resources/img/button_main.png").convert_alpha()
        self.btn_img_sub = pygame.image.load("./resources/img/button_sub.png").convert_alpha()

    @staticmethod
    def load_image(path):
        return pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))

    def read_output_file(self, index):
        filename = f"output-{index:02d}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                lines = f.readlines()
                # Giả sử dòng di chuyển là dòng cuối cùng trong file
                directions = lines[-1].strip()
                return directions
        else:
            print(f"File {filename} không tồn tại.")
            return ""

    # def run_game_from_output(self, index,method):
    #     index+=1
    #     filename=f"output-{index:02d}.txt"
    #     directions = support.read_path_from_file(method,filename)
    #     if directions:
    #         self.run_by_val(directions)
    #     else:

    #         print("Không tìm thấy lệnh di chuyển.")
    
    def initialize_stones(self):
        index = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.maze[row][col] == '$' or self.maze[row][col]=='*':
                    self.stone_data[(row, col)] = self.val[index]
                    index += 1

    def is_valid_move(self, new_row, new_col,next):
        return 0 <= new_row < ROWS and 0 <= new_col < COLS and self.maze[new_row][new_col] != next
    # def var_cham(self, dx, dy):
    #     new_row, new_col = self.player_pos[0] + dy, self.player_pos[1] + dx
    #     next_row, next_col = new_row + dy, new_col + dx
    #     if (self.maze[new_row][new_col] == '$' or self.maze[new_row][new_col] == '*' )and self.maze[next_row][next_col] in (' ', '.'):
    #         if self.maze[new_row][new_col] == '$':
    #             self.maze[new_row][new_col] = ' '
    #         else:
    #             self.maze[new_row][new_col]= '.'
    #         self.maze[next_row][next_col] = '$'
    #         #print(self.stone_data)
    #         self.stone_data[(next_row, next_col)] = self.stone_data.pop((new_row, new_col))
    def var_cham(self, dx, dy):
        # Tính toán vị trí mới cho người chơi
        new_row, new_col = self.player_pos[0] + dy, self.player_pos[1] + dx
        next_row, next_col = new_row + dy, new_col + dx
        
        # Kiểm tra nếu ô mới là đá và ô tiếp theo là trống hoặc đích
        if (self.maze[new_row][new_col] == '$' or self.maze[new_row][new_col] == '*') and self.maze[next_row][next_col] in (' ', '.'):
            # Xóa dấu đá ở vị trí hiện tại
            if self.maze[new_row][new_col] == '$':
                self.maze[new_row][new_col] = ' '
            else:
                self.maze[new_row][new_col] = '.'
            
            # Nếu ô tiếp theo là đích, biến đá thành '*', ngược lại giữ là '$'
            if self.maze[next_row][next_col] == '.':
                self.maze[next_row][next_col] = '*'  # Đá biến thành dấu '*' khi ở trên đích
            else:
                self.maze[next_row][next_col] = '$'  # Đá di chuyển bình thường
            
            # Cập nhật dữ liệu về vị trí đá trong `stone_data`
            self.stone_data[(next_row, next_col)] = self.stone_data.pop((new_row, new_col))

    def move_player(self, dx, dy):
        new_row, new_col = self.player_pos[0] + dy, self.player_pos[1] + dx
        if self.is_valid_move(new_row, new_col,'#'):
            self.var_cham(dx, dy)
            if (self.is_valid_move(new_row,new_col,'$')):
                if self.maze_original[self.player_pos[0]][self.player_pos[1]] in ('.',"*",'+'):
                    self.maze[self.player_pos[0]][self.player_pos[1]] = '.'
                else:
                    self.maze[self.player_pos[0]][self.player_pos[1]] = ' '
                self.player_pos = [new_row, new_col]
                self.maze[new_row][new_col] = '@'
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if self.is_handle and event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                continue
           
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: 
                    self.scroll_offset = max(self.scroll_offset - 20, 0)
                elif event.button == 5: 
                    max_offset = max(0, len(lst_maze) * BUTTON_HEIGHT - WINDOW_HEIGHT)
                    self.scroll_offset = min(self.scroll_offset + 20, max_offset)
    def draw_pause_overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  
        font = pygame.font.Font(None, 80) 
        text = font.render("PAUSE,", True, (255, 255, 255))  
        text2 = font.render("CLICK 'R'", True, (255, 255, 255))  
        text3 = font.render("TO RESTART", True, (255, 255, 255))  
        text_rect = text.get_rect(center=(900,50))
        overlay.blit(text, text_rect)
        text_rect2 = text.get_rect(center=(900,100))
        overlay.blit(text2, text_rect2)
        text_rect3 = text3.get_rect(center=(975,150))
        overlay.blit(text3, text_rect3)
        self.screen.blit(overlay, (0, 0))
        pygame.display.flip() 

    
    
    def show_popup(self, message):

        """Hiển thị cửa sổ popup với thông điệp."""
        popup_width, popup_height = 300, 100
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        # Vẽ nền cho popup
        pygame.draw.rect(self.screen, BLACK, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, WHITE, (popup_x + 5, popup_y + 5, popup_width - 10, popup_height - 10))

        # Vẽ thông điệp
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        
        # Chờ một khoảng thời gian hoặc cho đến khi người dùng nhấn một phím
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run_by_val(self, directions):
        if self.moving:
            return
        self.moving = True

        direction_map = {
            'l': (-1, 0),
            'r': (1, 0),
            'u': (0, -1),
            'd': (0, 1)
        }
        i=0
        if(directions=="" ):
            self.show_popup("Can't solve!, click 'esc'")
            self.chosen_algorithm = None
            self.moving = False
            return
        lst=support.findWeightNDisplay(directions,self.stone_data,self.player_pos)
       
        for direction in directions.lower():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  
                        self.paused = not self.paused
                        print("Pause" if self.paused else "Continue")
            if self.paused:
                self.draw_pause_overlay()
                while self.paused: 
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            self.paused = False
                            print("Tiếp tục di chuyển...")
                            break
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            self.paused = False
                            self.moving = False
                            self.restart_game()
                            return
                    pygame.time.wait(100) 
            if direction in direction_map:
                self.step+=1
                self.weight=lst[i]
                dx, dy = direction_map[direction]
                self.move_player(dx, dy)
                self.update_screen()
                pygame.display.flip()  
                pygame.time.wait(200) 
            i+=1

        self.moving = False

    
    def update_screen(self):
        self.screen.fill(GRAY_OUT)
        self.draw_buttons()
        self.draw_maze()
        pygame.display.flip()

    def move(self):
        keys = pygame.key.get_pressed()
        now = datetime.now()
        delay = 0.15
        if((now - self.last_move_time).total_seconds() >= delay):
        # if now - self.last_move_time >= MOVE_INTERVAL:
            if keys[pygame.K_UP]:
                self.move_player(0, -1)
            elif keys[pygame.K_DOWN]:
                self.move_player(0, 1)
            elif keys[pygame.K_LEFT]:
                self.move_player(-1, 0)
            elif keys[pygame.K_RIGHT]:
                self.move_player(1, 0)
            self.last_move_time = now

    def set_zero(self):
        self.step=0
        self.weight=0
    def restart_game(self):
        self.set_zero()
        self.maze, self.val = copy.deepcopy(lst_maze[self.current])
        self.maze_original = self.maze.copy()
        self.initialize_stones()
        tmp= find_object(self.maze, "@")
        self.player_pos = tmp if tmp!=None else find_object(self.maze, "+")
        self.chosen_algorithm = None
    
    def draw_maze(self):
        for row in range(ROWS):
            for col in range(COLS):
                x, y = col * TILE_SIZE + SIDEBAR_WIDTH, row * TILE_SIZE
                if self.maze[row][col] == '#':
                    self.screen.blit(self.block_img, (x, y))
                elif self.maze[row][col] in (' ', '$', '@', '.',"+","*"):
                    pygame.draw.rect(self.screen, GRAY_IN, (x, y, TILE_SIZE, TILE_SIZE))
                    if self.maze[row][col] == '$':
                        self.screen.blit(self.stone_img, (x, y))
                        stone_number = self.stone_data.get((row, col), "")
                        text_surface = self.font.render(stone_number, True, WHITE)
                        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                        self.screen.blit(text_surface, text_rect)
                    elif( self.maze[row][col]=="*"):
                        self.screen.blit(self.stone_img_2, (x, y))
                        stone_number = self.stone_data.get((row, col), "")
                        text_surface = self.font.render(stone_number, True, WHITE)
                        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                        self.screen.blit(text_surface, text_rect)                   
                    elif self.maze[row][col] == '@' or self.maze[row][col]=="+":
                        self.screen.blit(self.man_img, (x, y))
                    elif self.maze[row][col] == '.':
                        self.screen.blit(self.target_img, (x, y))
                pygame.draw.rect(self.screen, GRAY_LINE, (x, y, TILE_SIZE, TILE_SIZE), 1)
    def handle_algorithm(self,type_index):
        self.is_handle=True
        output = self.solve[type_index](*lst_maze[self.current])
        index=self.current+1
        filename=f"output-{index:02d}.txt"
        support.append_to_file(output,self.name_alg[type_index],filename)
        self.is_handle=False
        return 
    def display_current_maze_info(self):
        """Display information about the current maze."""
        current_index = self.current + 1  
        text = f"Current Maze: Input-{current_index:02}"
        text_surface = self.font_in_game.render(text, True, WHITE)  
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 20))  
        self.screen.blit(text_surface, text_rect)  
        
    def draw_buttons(self):
        """Draw the sidebar buttons."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        for i, _ in enumerate(lst_maze):
            y = i * BUTTON_HEIGHT - self.scroll_offset
            if -BUTTON_HEIGHT < y < WINDOW_HEIGHT:
                if self.current == i:
                    btn = self.bnt_img_sub1
                else:
                    btn = self.btn_img
                button = Button(btn, btn, (20, y + 15), 0.5)
            
                index=i+1
                
                text = f"Input-{index:02}"
                if (button.draw(self.screen, self.font_in_game, text, BLACK)) and not self.moving:
                    f = Fade(self.draw_maze, self.screen, pygame, BLACK, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    f.fade_out()
                    self.set_zero()
                    button.draw(self.screen, self.font_in_game, text, GRAY_IN)
                    self.maze, self.val = copy.deepcopy(lst_maze[i])
                    self.maze_original = self.maze.copy()
                    self.current = i
                    self.initialize_stones()
                    tmp= find_object(self.maze, "@")
                    self.player_pos = tmp if tmp!=None else find_object(self.maze, "+")
                    self.chosen_algorithm = None
                    f.fade_in()
           
       
        """Draw the downbar buttons."""
        # Nút để chạy 
        for i in range(len(self.name_alg)):
            btn=(Button(self.btn_img_sub, self.btn_img_sub, (320+i*100, 620), 1.5))
            color = RED if self.chosen_algorithm == self.name_alg[i] else BLACK
            if btn.draw(self.screen, self.font_in_game, "Run "+self.name_alg[i], color) and not self.moving:
                index=self.current+1
                filename=f"output-{index:02d}.txt"
                directions = support.read_path_from_file(self.name_alg[i],filename)
                if(directions is None):
                    self.handle_algorithm(i)
                    directions = support.read_path_from_file(self.name_alg[i],filename)
                    self.chosen_algorithm = self.name_alg[i]
                self.run_by_val(directions)
        btn_restart=(Button(self.bnt_restart, self.bnt_restart, (17, 620), 0.57))
        if btn_restart.draw(self.screen, self.font_in_game, "", BLACK) and not self.moving:
            self.restart_game()
        text_surface_step = self.font.render("Step:"+str(self.step), True, WHITE) 
        text_surface_cost = self.font.render("Cost:"+str(self.weight + self.step), True, WHITE)
        text_surface_weight = self.font.render("Weight:"+str(self.weight), True, WHITE) 
        text_rect_step = text_surface_step.get_rect(center=(1000, 620))
        text_rect_weight = text_surface_weight.get_rect(center=(1000, 650))
        text_rect_cost = text_surface_cost.get_rect(center=(1000, 680))

        self.screen.blit(text_surface_step, text_rect_step)
        self.screen.blit(text_surface_weight, text_rect_weight)
        self.screen.blit(text_surface_cost, text_rect_cost)
    def run(self):
        """Main chính alimi"""
        while True:
            self.handle_events()
            self.move()
            self.update_screen()
            self.display_current_maze_info()
if __name__ == "__main__":
    newGame=Game()
    #newGame.run_by_val("ulrd")
    newGame.run()