import pygame

# This class is a base class for all units in the game. (Player, enemies, etc.)
class Unit(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, sprites_path: str, speed: float=1, max_health=100, scale_factor: float=1):
        super().__init__()
        self._image_default = pygame.image.load(sprites_path + "/default.png").convert_alpha()
        self._image_hurt = pygame.image.load(sprites_path + "/hurt.png").convert_alpha()
        
        size = self._image_default.get_size()
        new_size = (int(size[0] * scale_factor), int(size[1] * scale_factor))
        
        self._image_default = pygame.transform.smoothscale(self._image_default, new_size)
        self._image_hurt = pygame.transform.smoothscale(self._image_hurt, new_size)
        
        self._max_health = max_health
        self._current_health = max_health
        self._speed = speed
        self._image_flipped = False
        self._hitbox = self._image_default.get_rect(topleft=pos)
        self._hurt_at = 0
        self._is_hurt = False
        self._attacks = []

    def move(self, dx, dy):
        if dx > 0:
            self._image_flipped = True
        elif dx < 0:
            self._image_flipped = False
        
        self._hitbox.x += dx * self._speed
        self._hitbox.y += dy * self._speed

    def heal(self, amount = 0):
        if self._current_health + amount > self._max_health:
            self._current_health = self._max_health
        else:
            self._current_health += amount

    def take_damage(self, amount):
        if self._current_health - amount < 0:
            self._current_health = 0
        else:
            self._current_health -= amount  
            
        self._is_hurt = True
        self._hurt_at = pygame.time.get_ticks()
        return self._current_health
    
    def display_health_bar(self):
        health_ratio = self._current_health / self._max_health
        
        x = self._hitbox.x + self._hitbox.width // 2 - 15
        y = self._hitbox.y + self._hitbox.height
        
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, 30, 5), border_radius=2)
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, 30 * health_ratio, 5), border_radius=2)
    
    def get_pos(self):
        return pygame.Vector2(self._hitbox.topleft)
    
    def collides_with(self, _hitbox):
        return self._hitbox.colliderect(_hitbox)
    
    def add_attack(self, attack):
        self._attacks.append(attack)

    def find_attack(self, callback):
        for attack in self._attacks:
            if callback(attack):
                return attack
        

    @property
    def is_dead(self):
        return self._current_health <= 0
    
    @property
    def health(self):
        return self._current_health
    
    # will be called each frame
    def update(self, game):
        time = pygame.time.get_ticks()
        if self._is_hurt and time <= self._hurt_at + 100:
            image = pygame.transform.flip(self._image_hurt, True, False) if self._image_flipped else self._image_hurt
        else:
            image = pygame.transform.flip(self._image_default, True, False) if self._image_flipped else self._image_default
            self._is_hurt = False
            
        game._screen.blit(image, self._hitbox.topleft)

        for attack in self._attacks:
            attack.update(game)
            
        