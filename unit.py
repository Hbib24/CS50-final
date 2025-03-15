import pygame

# This class is a base class for all units in the game. (Player, enemies, etc.)
class Unit(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image_path: str, speed=1, max_health=100, scale_factor: float=1):
        super().__init__()  # Initialize Sprite class
        self._max_health = max_health
        self._current_health = max_health
        self._speed = speed
        self._image = pygame.image.load(image_path).convert_alpha()
        self._image_flipped = False
        self._attacks = []

        size = self._image.get_size()
        new_size = (int(size[0] * scale_factor), int(size[1] * scale_factor))
        
        self._image = pygame.transform.smoothscale(self._image, new_size)
        self.hitbox = self._image.get_rect(topleft=pos)

    def move(self, dx, dy):
        if dx > 0:
            self._image_flipped = True
        elif dx < 0:
            self._image_flipped = False
        
        self.hitbox.x += dx * self._speed
        self.hitbox.y += dy * self._speed

    def take_damage(self, amount):
        self._current_health -= amount  
        return self._current_health    
    
    def get_pos(self):
        return pygame.Vector2(self.hitbox.topleft)
    
    def collides_with(self, hitbox):
        return self.hitbox.colliderect(hitbox)
    
    def add_attack(self, attack):
        self._attacks.append(attack)
        

    @property
    def is_dead(self):
        return self._current_health <= 0
    
    @property
    def health(self):
        return self._current_health
    
    # will be called each frame
    def update(self, game):
        image = pygame.transform.flip(self._image, True, False) if self._image_flipped else self._image
        
        game._screen.blit(image, self.hitbox.topleft)

        for attack in self._attacks:
            attack.update(game)
            
        