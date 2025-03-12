import pygame

class Attack:
    def __init__(self, owner, cooldown=1000, damage=10):
        self.owner = owner  # The unit that owns this attack (Player, Mob, etc.)
        self.cooldown = cooldown
        self.damage = damage
        self.last_attack_time = 0  # Track when the last attack happened

    def can_attack(self, current_time):
        return current_time - self.last_attack_time >= self.cooldown

    def perform_attack(self, current_time, *args, **kwargs):
        """This will be overridden by specific attack types."""
        if self.can_attack(current_time):
            self.last_attack_time = current_time
            self.execute(*args, **kwargs)

    def execute(self, *args, **kwargs):
        """Override in subclasses for specific attack behavior."""
        pass
