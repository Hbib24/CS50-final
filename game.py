import pygame

from mob_spawer import MobSpawner
from player import Player
from ui import UI

class Game:
    _dt = 0

    def __init__(self, fullscreen=False):
        pygame.init()

        flags = 0
        if fullscreen:
            flags = pygame.FULLSCREEN

        self._screen = pygame.display.set_mode((1280, 720), flags=flags)
        self._clock = pygame.time.Clock()
        self._timer = 0
        self._score = 0 # score = mob kill count
        self._level = 1 # each level has increased mob spawn frequency

    def init_player(self):
        self._player = Player(self._screen)

    def init_mob_generator(self):
        self._mob_generator = MobSpawner(self._screen, self._player)
    
    def init_ui(self):
        self._ui = UI(self._screen, self._player)

    def increment_score(self, amount = 1):
        self._score += amount

    def increment_level(self, by = 1):
        self._level += by

    def run(self):
        self.init_player()
        self.init_mob_generator()
        self.init_ui()
        self._running = True

        while self._running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # fill the screen with a color to wipe away anything from last frame
            self._screen.fill("gray")

            # ================= GAME LOGIC =================== #
            if self._player.is_dead:
                self._ui.display_game_over(self._timer, self._score)
                pygame.display.flip()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.run()
                elif keys[pygame.K_q]:
                    pygame.quit()
                    
            else:
                self._ui.draw(self._timer, self._level, self._score) 

                self._player.handle_movement()
                self._player.draw()
                attack_pos = self._player.trigger_sword_attack()

                self._mob_generator.update(self._dt, self.increment_level, self.increment_score, attack_pos)
                self._mob_generator.draw_mobs(self._dt)
                
                self._timer += 1 / 60

            # flip() the display to put your work on screen
            pygame.display.flip()
            self._dt = self._clock.tick(60)

        pygame.quit()

    