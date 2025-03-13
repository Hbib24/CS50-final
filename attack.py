import pygame
from unit import Unit

class Attack(pygame.sprite.Sprite):
    def __init__(self, owner: Unit, target: Unit, cooldown=1000, damage=10, duration=500):
        super().__init__()
        self.cooldown = cooldown
        self.damage = damage
        self.duration = duration
        self.target = target
        self.owner = owner
        self.last_attack_time = 0
        self.attack_start_time = 0  # Track when attack starts
        self.active = False
        
    def can_attack(self, current_time):
        return (current_time - self.last_attack_time) >= self.cooldown and not self.active
        
    def update(self, current_time, screen: pygame.Surface):
        if self.can_attack(current_time):
            self.last_attack_time = current_time
            self.attack_start_time = current_time
            self.active = True  # Activate attack

        if self.active:
            self.trigger(screen)

            # Disable attack after duration
            if (current_time - self.attack_start_time) >= self.duration:
                self.active = False  
                
    def trigger(self, screen):
        pass
