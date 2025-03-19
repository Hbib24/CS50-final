import pygame
from attacks.attack import Attack
from unit import Unit

class AreaAttack(Attack):
    def __init__(self, owner: Unit, targets: list, cooldown=500, damage=10, duration=100, radius=100):
        super().__init__(owner, targets, cooldown, damage, duration)
        
        self.radius = radius 
        self.hitbox = pygame.Rect(0, 0, radius * 2, radius * 2)
        
        
    def update(self, game):
        ...