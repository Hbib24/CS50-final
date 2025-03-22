import pygame

from ability_manager import AbilityManager
from event_manager import EventManager
from mobs.mob_manager import MobManager
from player import Player
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
        self._level_up = False
        self._dt = 0
        self._timer = 0 # in seconds
        self._event_manager = EventManager()
        self._player = Player(self)
        self._mob_manager = MobManager()
        self._ability_manager = AbilityManager(self)
        self._ui = UI(self._screen, self)

    def run(self):
        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                self._event_manager.handle_event(event)
                if event.type == pygame.QUIT:
                    self._running = False
                    break

                if event.type == pygame.KEYDOWN and self._level_up:
                    self._player.pick_ability(event.key)
                
                if event.type == pygame.KEYDOWN and not self._level_up: 
                    if event.key == pygame.K_ESCAPE:
                        self.pause()

                    if self._over or self._paused:
                        if event.key == pygame.K_r:
                            self.restart()
                        if event.key == pygame.K_q:
                            self._running = False
                            break

            # ================== RENDER YOUR GAME HERE ================== #
            if self._over:
                self._ui.pop_up("game over")
                self._ui.display_controls()
                
            if not self._paused and not self._over and not self._level_up:
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

    def pause(self):
        self._paused = not self._paused
        self._ui.pop_up("paused", width=550)
        self._ui.display_tips()
        self._ui.display_controls()

    def restart(self):
        self.init()
        self.run()