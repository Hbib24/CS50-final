import pygame
from unit import Unit

class Attack():
    def __init__(self, owner: Unit, targets: list, cooldown=1000, damage=1, duration=500):
        self.cooldown = cooldown
        self.damage = damage
        self.duration = duration
        self.targets = targets
        self.owner = owner
        self.last_attack_time = 0

    # check cooldown
    def can_attack(self):
        return pygame.time.get_ticks() - self.last_attack_time >= self.cooldown
    
    def add_target(self, target: Unit):
        self.targets.append(target)
