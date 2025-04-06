import pygame

from src.unit import Unit
from src.attacks.attack import Attack

class SwordAttack(Attack):
    def __init__(self, owner: Unit, targets: list, duration=400, damage=5, cooldown=1500):
        super().__init__(owner, targets, cooldown, damage, duration)
        
        self.image = pygame.image.load("assets/attacks/sword.png").convert_alpha()
        self.hitbox = self.image.get_rect()
        
    def update_pos(self):
        owner_pos = self.owner.get_pos()
        
        if self.owner._image_flipped:
            self.hitbox.x = owner_pos.x + 50
        else:
            self.hitbox.x = owner_pos.x - self.owner._hitbox.width - 50
            
        self.hitbox.y = owner_pos.y + (self.owner._hitbox.height / 2) - (self.hitbox.height / 2)
        

    def update(self, game):

        if self.can_attack():
            self.attack()  

        if self.is_attacking():
            self.update_pos()
            image = pygame.transform.flip(self.image, True, False) if self.owner._image_flipped else self.image
            game._screen.blit(image, self.hitbox.topleft)

            for target in self.targets:
                if not target.is_dead and self.hitbox.colliderect(target._hitbox):
                    target.take_damage(self.damage)

