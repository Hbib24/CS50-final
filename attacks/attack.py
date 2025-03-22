import pygame
from unit import Unit

class Attack():
    def __init__(self, owner: Unit, targets: list, cooldown:float=1000, damage:float=1, duration:float=500):
        self.cooldown = cooldown
        self.damage = damage
        self.duration = duration
        self.targets = targets
        self.owner = owner
        self.last_attack_time = 0

    # check cooldown
    def can_attack(self):
        time = pygame.time.get_ticks()
        return self.last_attack_time == 0 or time >= self.last_attack_time + self.cooldown
    
    def is_attacking(self):
        time = pygame.time.get_ticks()
        return time - self.last_attack_time < self.duration
    
    def attack(self):
        time = pygame.time.get_ticks()
        self.last_attack_time = time
    
    def add_target(self, target: Unit):
        self.targets.append(target)
