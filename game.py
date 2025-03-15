import pygame

from mobs.mob_manager import MobManager
from player import Player
from mobs.basic_mob import BasicMob
from attacks.proximity_attack import ProximityAttack
from attacks.sword_attack import SwordAttack
from ui import UI

class Game:
    def __init__(self, fullscreen=False):
        # pygame setup
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._running = True
        self._paused = False
        self._over = False
        self._dt = 0
        self._timer = 0 # in seconds
        self._player = Player(self._screen)
        self._player.add_attack(SwordAttack(self._player, []))
        self._mob_manager = MobManager()
        self._ui = UI(self._screen)

    def run(self):
        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # fill the screen with a color to wipe away anything from last frame
            self._screen.fill("gray")

            # ================== RENDER YOUR GAME HERE ================== #
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_ESCAPE]:
                self._paused = not self._paused
            
            if not self._paused and not self._over:
                self._player.update(self)
                self._mob_manager.spawn_basics(self)

                self._ui.display_game_ui(self)



            # flip() the display to put your work on screen
            pygame.display.flip()
            self._timer += 1 / 60
            self._dt = self._clock.tick(60) / 1000  # limits FPS to 60

        pygame.quit()