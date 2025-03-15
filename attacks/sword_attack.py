import pygame

from unit import Unit
from attack import Attack

class SwordAttack(Attack):
    def __init__(self, owner: Unit, targets: tuple, duration=400, damage=5):
        super().__init__(owner, targets, duration, damage)
        
        self.image = pygame.image.load("assets/attacks/sword.png").convert_alpha()
        self.hitbox = self.image.get_rect()
        
    def update_pos(self):
        owner_pos = self.owner.get_pos()
        
        if self.owner._image_flipped:
            self.hitbox.x = owner_pos.x + 50
        else:
            self.hitbox.x = owner_pos.x - self.owner.hitbox.width - 50
            
        self.hitbox.y = owner_pos.y + (self.owner.hitbox.height / 2) - (self.hitbox.height / 2)
        

    def update(self, game):
        time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.last_attack_time == 0:
            self.last_attack_time = time

        # If the attack has been triggered and within the duration window, it's active
        if self.last_attack_time != 0 and time - self.last_attack_time < self.duration:
            self.update_pos()
            image = pygame.transform.flip(self.image, True, False) if self.owner._image_flipped else self.image
            
            game._screen.blit(image, self.hitbox.topleft)
            pygame.draw.rect(game._screen, "red", self.hitbox, 1)  # Debug hitbox

            # Check for collision with targets
            for target in self.targets:
                if self.hitbox.colliderect(target.hitbox):
                    target.take_damage(self.damage)
        else:
            # Reset attack when the duration has passed
            self.last_attack_time = 0
