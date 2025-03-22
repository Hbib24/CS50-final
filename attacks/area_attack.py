import pygame
from attacks.attack import Attack
from unit import Unit

class AreaAttack(Attack):
    def __init__(self, owner: Unit, targets: list, cooldown=500, damage=10, duration=100, radius=100):
        super().__init__(owner, targets, cooldown, damage, duration)
        
        self.radius = radius 
        self.hitbox = pygame.Rect(0, 0, radius * 2, radius * 2)
        
        
    def update(self, game):
        self.hitbox.center = self.owner._hitbox.center
        aoe_surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)
        pygame.draw.circle(aoe_surface, (150, 0, 0, 30), (self.radius, self.radius), self.radius)
        game._screen.blit(aoe_surface, (self.hitbox.x, self.hitbox.y))
        
        if self.can_attack():
            for target in self.targets:
                if self.hitbox.colliderect(target._hitbox):
                    target.take_damage(self.damage)
                    self.attack()