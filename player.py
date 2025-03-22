import random
import pygame
import json

from event_manager import Event
from unit import Unit

class Player(Unit):
    def __init__(self, game):
        pos = (game._screen.get_width() // 2, game._screen.get_height() // 2) # center of the screen
        super().__init__(pos, speed=3, sprites_path="assets/player", scale_factor=1.5)
        
        self.screen = game._screen
        self.game = game
        self.level = 1
        self.experience = 0
        self.levelup_experience = 100 # required experience for lvl up
        
        game._event_manager.listen_to(Event.MOB_KILL, self.gain_experience)
        game._event_manager.listen_to(Event.LEVEL_UP, self.on_level_up)
        
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
            
    def gain_experience(self, _):
        self.experience += 100
        
        if self.experience >= self.levelup_experience:
            self.level += 1
            self.experience -= self.levelup_experience
            self.levelup_experience += 50
            self.game._event_manager.post_event(Event.LEVEL_UP)

    def get_random_powers(self):
        power_ups: list = self.get_powers()
        choices = []

        for _ in range(3):
            pwr = random.choice(power_ups)

            power_ups.pop(power_ups.index(pwr))
            choices.append(pwr)

        return choices

    def on_level_up(self, _):
        self.powers = self.get_random_powers()
        self.game._level_up = True
        self.game._ui.level_up(self.powers)

    def pick_ability(self, key):
        if key == pygame.K_1:
            self.game._event_manager.post_event(Event.ABILITY_PICK, self.powers[0])
            self.game._level_up = False
        elif key == pygame.K_2:
            self.game._event_manager.post_event(Event.ABILITY_PICK, self.powers[1])
            self.game._level_up = False
        elif key == pygame.K_3:
            self.game._event_manager.post_event(Event.ABILITY_PICK, self.powers[2])
            self.game._level_up = False
    
                
    def get_powers(self):
        with open("assets/ui/power_ups.json", "r") as file:
            return json.load(file)
                    
    # will be called each frame
    def update(self, game):
        if self.is_dead:
            game._over = True
                        

        self.handle_movement()
        super().update(game)
        