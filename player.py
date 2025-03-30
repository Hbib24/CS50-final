import pygame

from event_manager import Event
from unit import Unit

class Player(Unit):
    def __init__(self, game):
        pos = (game._screen.get_width() // 2, game._screen.get_height() // 2) # center of the screen
        super().__init__(pos, speed=1.5, sprites_path="assets/player", scale_factor=1.5)
        
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
            self.game._event_manager.post_event(Event.PLAYER_MOVE, (-1, 0))
            self.flip(False)
        if keys[pygame.K_RIGHT]:
            self.game._event_manager.post_event(Event.PLAYER_MOVE, (1, 0))
            self.flip()
        if keys[pygame.K_UP]:
            self.game._event_manager.post_event(Event.PLAYER_MOVE, (0, -1))
        if keys[pygame.K_DOWN]:
            self.game._event_manager.post_event(Event.PLAYER_MOVE, (0, 1))
            
    def gain_experience(self, mob):
        match mob.data.get("type"):
            case "basic":
                self.experience += 20
            case "special":
                self.experience += 50
        
        if self.experience >= self.levelup_experience:
            self.level += 1
            self.experience -= self.levelup_experience
            self.levelup_experience += 50
            self.game._event_manager.post_event(Event.LEVEL_UP)


    def on_level_up(self, _):
        powers = self.game._ability_manager.get_random_powers()
        self.game._ability_manager.rand_powers = powers
        self.game._level_up = True
        self.game._ui.level_up(powers)
                    
    # will be called each frame
    def update(self, game):
        if self.is_dead:
            game._over = True
                        

        self.handle_movement()
        super().update(game)
        