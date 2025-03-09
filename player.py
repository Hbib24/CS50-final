import pygame
from unit import Unit
import os

class Player(Unit):
    ATTACK_COOLDOWN = 700
    ATTACK_DURATION = 300
    ATTACK_RANGE = 100

    def __init__(self, screen):
        # init player in the center of the screen
        super().__init__(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
        self._screen = screen
        self._attack_cooldown = self.ATTACK_COOLDOWN # cooldown between attacks
        self._attack_duration = self.ATTACK_DURATION 
        self.attack_frames = self.load_attack_animation("assets/player_attack/")

    def draw(self):
        pygame.draw.circle(self._screen, "blue", self._pos, 10)

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)

    def load_attack_animation(self, folder_path):
        frames = []
        for file in sorted(os.listdir(folder_path)):  # Ensure order
            if file.endswith(".png"):
                frame = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
                frames.append(pygame.transform.scale(frame, (80, 80)))  # Resize if needed
        return frames

    def trigger_sword_attack(self):
        if self._attack_duration <= 0:
            self._attack_cooldown -= 10
        self._attack_duration -= 10

        # If cooldown is over, start an attack
        if self._attack_cooldown <= 0 and self._attack_duration <= 0:
            self._attack_cooldown = self.ATTACK_COOLDOWN  # Reset cooldown after attack disappears
            self._attack_duration = self.ATTACK_DURATION  # Start attack

        # While the attack is active, draw the attack line
        if self._attack_duration > 0:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            direction = mouse_pos - self._pos
            if direction.length() != 0:
                direction = direction.normalize()

            attack_length = direction * self.ATTACK_RANGE 
            attack_end = self._pos + attack_length
            
            pygame.draw.line(self._screen, "yellow", self._pos, attack_end, 5)

            self._attack_duration -= 10
            return attack_end
    
    def trigger_sphere_attack(self):
        ...
       

        
        
