import pygame

from player import Player
from basic_mob import BasicMob
from attacks.proximity_attack import ProximityAttack
from attacks.slash_attack import SlashAttack

class Game:
    def __init__(self, fullscreen=False):
        # pygame setup
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._running = True
        self._paused = False
        self._dt = 0
        self._timer = 0 # in seconds
        self._player = Player(self._screen)
        self._mob = BasicMob(self._screen)
        self._slashAttack = SlashAttack(self._player, (self._mob,))

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
            
            if not self._paused:
                self._player.update(self)
                self._slashAttack.update(self)
                if not self._mob.is_dead:
                    self._mob.update(self)


            # flip() the display to put your work on screen
            pygame.display.flip()
            self._timer += 1 / 60
            self._dt = self._clock.tick(60) / 1000  # limits FPS to 60

        pygame.quit()