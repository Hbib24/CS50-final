import pygame

from attacks.area_attack import AreaAttack
from event_manager import EventManager
from mobs.mob_manager import MobManager
from player import Player
from attacks.sword_attack import SwordAttack
from ui import UI

class Game:
    def __init__(self, fullscreen=False):
        # pygame setup
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._running = True
        self.init()

        
    def init(self):
        self._paused = False
        self._over = False
        self._dt = 0
        self._timer = 0 # in seconds
        self._event_manager = EventManager()
        self._player = Player(self)
        self._player.add_attack(SwordAttack(self._player, []))
        self._player.add_attack(AreaAttack(self._player, []))
        self._mob_manager = MobManager()
        self._ui = UI(self._screen, self)
        # pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

    def run(self):
        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                self._event_manager.handle_event(event)
                if event.type == pygame.QUIT:
                    self._running = False
                
                if event.type == pygame.KEYDOWN:  # Detects key press only once per press
                    if event.key == pygame.K_ESCAPE:
                        self._paused = not self._paused
                        self._ui.pop_up("paused", "paused")
                    if event.key == pygame.K_r and self._over:
                        self.init()
                        self.run()


            # ================== RENDER YOUR GAME HERE ================== #
            if self._over:
                self._ui.pop_up("game over", "game over")
                
            if not self._paused and not self._over:
                # fill the screen with a color to wipe away anything from last frame
                self._screen.fill("gray")
                self._ui.backdrop_active = False
                self._player.update(self)
                self._mob_manager.spawn_basics(self)
                self._ui.display_game_ui(self)



            # flip() the display to put your work on screen
            pygame.display.flip()
            self._timer += 1 / 60
            self._dt = self._clock.tick(60) / 1000


        pygame.quit()