import pygame
import random

from unit import Unit

class BasicMob(Unit):
    def __init__(self, screen: pygame.Surface, max_health=100, sprites_path=None, scale_factor=1.5, speed=None):
        self.screen = screen

        if not sprites_path:
            mobs = ["orc", "slime"]
            sprites_path = f"assets/{random.choice(mobs)}"
        
        if not speed:
            speed = self.get_random_speed()

        super().__init__(self.get_random_pos(), speed=speed, sprites_path=sprites_path, scale_factor=scale_factor, max_health=max_health)
        
        
    def get_random_speed(self) -> float:
        return random.uniform(1.6, 2.2)
        
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
        self.display_health_bar()
        super().update(game)
        