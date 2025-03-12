import pygame

from unit import Unit

class Player(Unit):
    def __init__(self, screen: pygame.Surface):
        pos = (screen.get_width() // 2, screen.get_height() // 2) # center of the screen
        super().__init__(pos, speed=5, image_path="assets/player/player.png", scale_factor=1.5)
        
        self.screen = screen
        self.level = 1
        
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
            
    # will be called each frame
    def update(self, game):
        self.handle_movement()
        super().update(self.screen)
        