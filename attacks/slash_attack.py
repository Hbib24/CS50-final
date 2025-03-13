import pygame

from unit import Unit

class SlashAttack():
    def __init__(self, owner: Unit, targets: tuple, duration=1000, damage=5):
        self.owner = owner
        self.duration = duration
        self.targets = targets
        self.damage = damage
        self.last_attack_time = 0
        
        owner_pos = self.owner.hitbox.topleft
        self.image = pygame.image.load("assets/attacks/slash/2.png").convert_alpha()
        self.hitbox = pygame.Rect(owner_pos[0], owner_pos[1], 50, 20)
        
    def update_pos(self):
        owner_pos = self.owner.get_pos()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        direction = mouse_pos - owner_pos
        
        if direction.length() > 0:
            direction = direction.normalize()
            self.hitbox.x = owner_pos[0] + direction.x * 50
            self.hitbox.y = owner_pos[1] + direction.y * 50

    def update(self, game):
        time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.last_attack_time == 0:
            self.last_attack_time = time

        # If the attack has been triggered and within the duration window, it's active
        if self.last_attack_time != 0 and time - self.last_attack_time < self.duration:
            self.update_pos()
            pygame.draw.rect(game._screen, "red", self.hitbox, 1)  # Debug hitbox

            # Check for collision with targets
            for target in self.targets:
                if self.hitbox.colliderect(target.hitbox):
                    target.take_damage(self.damage)
        else:
            # Reset attack when the duration has passed
            self.last_attack_time = 0
