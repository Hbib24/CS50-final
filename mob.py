import pygame
import random
from unit import Unit

class Mob(Unit):
    ATTACK_COOLDOWN = 300
    
    def __init__(self, screen, player):
        super().__init__(pos=self.get_pos(screen), speed=self.get_speed())
        self._screen = screen
        self._player = player
        self._attack_cooldown = self.ATTACK_COOLDOWN # cooldown between attacks

    # randomize speed
    def get_speed(self):
        return random.uniform(1.5, 2.5)
    
    # randomize mob spawn position from the edges of the screen
    def get_pos(self, screen):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            x = random.randint(0, screen.get_width())
            y = 0  
        elif edge == 'bottom':
            x = random.randint(0, screen.get_width())
            y = screen.get_height() 
        elif edge == 'left':
            x = 0
            y = random.randint(0, screen.get_height())
        elif edge == 'right':
            x = screen.get_width() 
            y = random.randint(0, screen.get_height())

        return pygame.Vector2(x, y)

    def draw(self):
        if not self.is_dead:
            pygame.draw.circle(self._screen, "red", self._pos, 10)

    def handle_attacked(self, attack_pos):
        dx = attack_pos.x - self._pos.x
        dy = attack_pos.y - self._pos.y

        distance = pygame.math.Vector2(dx, dy).length()

        if distance <= 10:
            self.take_damage(self._max_health)
            return True
        return False


    def attack_player(self, dt):
        self._attack_cooldown -= dt
        dx = self._player._pos.x - self._pos.x
        dy = self._player._pos.y - self._pos.y

        # calculate the distance between the mob and player
        distance = pygame.math.Vector2(dx, dy).length()
        
        if distance <= 10 and self._attack_cooldown <= 0:
            self._player.take_damage(5)
            self._attack_cooldown = self.ATTACK_COOLDOWN


    def chase_player(self):
        dx = self._player._pos.x - self._pos.x
        dy = self._player._pos.y - self._pos.y
        if dx != 0:
            dx = dx / abs(dx)
        if dy != 0:
            dy = dy / abs(dy)
        
        self.move(dx, dy)
