import pygame
import math
from attacks.attack import Attack
from unit import Unit

class RotatingAttack(Attack):
    def __init__(self, owner: Unit, targets: list, cooldown=0, damage=3, duration=100, radius=100, speed=2, shuriken_count=1):
        super().__init__(owner, targets, cooldown, damage, duration)
        
        self.image = pygame.image.load("assets/attacks/shuriken.png").convert_alpha()
        self.radius = radius  
        self.speed = speed  
        self.shuriken_count = shuriken_count  # Number of shurikens
        self.angles = [i * (360 / shuriken_count) for i in range(shuriken_count)]  # Equally spaced angles
        self.hitboxes = [self.image.get_rect() for _ in range(shuriken_count)]  # One hitbox per shuriken

    def upgrade(self, new_speed=None, extra_shurikens=0):
        """Upgrades the attack by increasing speed and/or adding more shurikens."""
        if new_speed:
            self.speed = new_speed  # Increase rotation speed
        if extra_shurikens > 0:
            new_angles = [i * (360 / (self.shuriken_count + extra_shurikens)) for i in range(self.shuriken_count + extra_shurikens)]
            self.angles = new_angles  # Recalculate angles to spread them evenly
            self.hitboxes = [self.image.get_rect() for _ in new_angles]  # Create new hitboxes
            self.shuriken_count += extra_shurikens

    def update(self, game):
        """Moves all shurikens in a circular pattern and applies damage on collision."""
        for i in range(self.shuriken_count):
            self.angles[i] += self.speed  # Rotate each shuriken
            
            if self.angles[i] >= 360:
                self.angles[i] -= 360

            # Calculate position
            center_x = self.owner._hitbox.centerx + self.radius * math.cos(math.radians(self.angles[i]))
            center_y = self.owner._hitbox.centery + self.radius * math.sin(math.radians(self.angles[i]))

            # Update hitbox position
            self.hitboxes[i].center = (center_x, center_y)

            # Rotate shuriken image
            rotated_image = pygame.transform.rotate(self.image, -self.angles[i])
            rotated_rect = rotated_image.get_rect(center=self.hitboxes[i].center)

            # Draw shuriken
            game._screen.blit(rotated_image, rotated_rect.topleft)

        # Check for collisions
        if self.can_attack():
            for target in self.targets:
                for hitbox in self.hitboxes:
                    if hitbox.colliderect(target._hitbox):
                        target.take_damage(self.damage)
            self.attack()  # Reset cooldown
