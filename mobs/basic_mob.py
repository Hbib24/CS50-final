import pygame
import random

from unit import Unit

class BasicMob(Unit):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        super().__init__(self.get_random_pos(), speed=self.get_random_speed(), image_path="assets/mobs/basic_mob.png", scale_factor=1.5)
        
        
    def get_random_speed(self) -> float:
        return random.uniform(1.5, 2.5)
        
    def get_random_pos(self) -> tuple:
        edges = ["top", "right", "bottom", "left"]
        edge = random.choice(edges)
        
        if edge == "top":
            return (random.randint(0, self.screen.get_width()), self.screen.get_height())
        elif edge == "right":
            return (self.screen.get_width(), random.randint(0, self.screen.get_height()))
        elif edge == "bottom":
            return (random.randint(0, self.screen.get_width()), 0)
        else:
            return (0, random.randint(0, self.screen.get_height()))
        
    def handle_movement(self, player_pos: pygame.Vector2):
        direction = player_pos - self.get_pos()
        if direction.length() > 0:
            direction = direction.normalize()
            self.move(direction.x, direction.y)
            
    # will be called each frame
    def update(self, game):
        self.handle_movement(game._player.get_pos())
        super().update(game)
        