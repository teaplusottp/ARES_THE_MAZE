import pygame
from .support import images_are_equal


class Button:
    def __init__(self, img_normal, img_clicked, pos, scale):
        w, h = img_normal.get_width(), img_normal.get_height()
        self.img_normal = pygame.transform.scale(img_normal, (int(w * scale), int(h * scale)))
        self.img_clicked = pygame.transform.scale(img_clicked, (int(w * scale), int(h * scale)))  
        self.rect = self.img_normal.get_rect()
        self.rect.topleft = pos
        self.clicked = False
        self.hovered = False 

    def draw(self, surface, font, text, text_color):
        action = False
        pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(pos)
        if self.clicked:
            surface.blit(self.img_clicked, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.img_normal, (self.rect.x, self.rect.y))
            if self.hovered and images_are_equal(self.img_clicked,self.img_normal):
                pygame.draw.rect(surface, (188, 230, 156), self.rect)  
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        return action

# pygame.init()
# screen = pygame.display.set_mode((600, 400))
# pygame.display.set_caption("Hover Window Example")
# clock = pygame.time.Clock()

# main_button_img = pygame.Surface((100, 50)) 
# main_button_img.fill((0, 200, 0))
# main_button = Button(main_button_img, (50, 50), 1)

# sub_buttons = [
#     Button(main_button_img, (0, 0), 0.8),
#     Button(main_button_img, (0, 0), 0.8),
#     Button(main_button_img, (0, 0), 0.8),
# ]

# hover_win = Hover_Win(sub_buttons, (150, 50))

# running = True
# while running:
#     screen.fill((30, 30, 30))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     if main_button.draw(screen, pygame.font.SysFont(None, 24), "Main", (255, 255, 255)):
#         print("Main button clicked")

#     hover_win.visible = main_button.hovered or hover_win.is_hovered(pygame.mouse.get_pos())

#     hover_win.show(screen)

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
