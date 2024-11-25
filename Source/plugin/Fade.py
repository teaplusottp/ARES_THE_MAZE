class Fade:
    def __init__(self,alterFunc,surface,pygame,fillColor,size):
        self.alterFunc=alterFunc
        self.surface=surface
        self.pygame=pygame
        self.fillColor=fillColor
        self.size=size
    def fade_in(self):
        fade = self.pygame.Surface(self.size)
        fade.fill(self.fillColor)
        for alpha in range(0, 300, 5):
            fade.set_alpha(300 - alpha)
            self.alterFunc()
            self.surface.blit(fade, (0, 0))
            self.pygame.display.update()
            self.pygame.time.delay(10)
    def fade_out(self):
        fade = self.pygame.Surface(self.size)
        fade.fill(self.fillColor)
        for alpha in range(0, 300, 5):
            fade.set_alpha(alpha)
            self.alterFunc()
            self.surface.blit(fade, (0, 0))
            self.pygame.display.update()
            self.pygame.time.delay(10)