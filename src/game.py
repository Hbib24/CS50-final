import pygame

from src.ability_manager import AbilityManager
from src.audio_manager import AudioManager
from src.background import Background
from src.event_manager import Event, EventManager
from src.mobs.mob_manager import MobManager
from src.player import Player
from src.ui.ui import UI
from src.firestore import Firestore

class Game:
    TITLE = "PyRogue"
    VERSION = "0.0.1"

    def __init__(self, fullscreen=False, offline=False):
        # pygame setup
        pygame.init()
        pygame.display.set_icon(pygame.image.load("assets/player/default.png"))
        pygame.display.set_caption(f"{self.TITLE} - v{self.VERSION}")
        self._screen = pygame.display.set_mode((1280, 720), flags=pygame.FULLSCREEN if fullscreen else 0)
        self._clock = pygame.time.Clock()
        self._running = True
        self._offline = offline

        self._world_width = self._screen.get_width() * 3
        self._world_height = self._screen.get_height() * 3
        self._world_start = pygame.Vector2(-(self._world_width / 2) + self._screen.get_width() / 2, -(self._world_height / 2) + self._screen.get_height() / 2)
        self._world_end = pygame.Vector2(self._world_width / 2 - self._screen.get_width() / 2, self._world_height / 2 - self._screen.get_height() / 2)
        self._firestore = Firestore(self) if not self._offline else None
        self._player_name = None

        self._menu = True
        self.init()

    def init(self):
        self._paused = False
        self._over = False
        self._level_up = False
        self._scored_saved = False
        self._event_manager = EventManager()
        self._audio_manager = AudioManager(self)
        self._ui = UI(self._screen, self)
        self._dt = 0
        self._timer = 0 # in seconds
        self._player = Player(self)
        self._mob_manager = MobManager()
        self._ability_manager = AbilityManager(self)
        self._background = Background(self)

        
    def start(self):
        self._menu = False
        self.init()

    def run(self):
        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                self._event_manager.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._event_manager.post_event(Event.MOUSE_CLICK, event)
                if event.type == pygame.KEYDOWN:
                    self._event_manager.post_event(Event.KB_DOWN, event)
                    
                if event.type == pygame.QUIT:
                    self._running = False
                    break

                if event.type == pygame.KEYDOWN and self._level_up:
                    self._ability_manager.on_player_pick(event.key)
                
                if event.type == pygame.KEYDOWN and not self._level_up and not self._menu: 
                    if event.key == pygame.K_ESCAPE:
                        self.pause()

                    if self._over or self._paused:
                        if event.key == pygame.K_r:
                            self.restart()
                        if event.key == pygame.K_q:
                            self._menu = True

            # ================== RENDER YOUR GAME HERE ================== #
            if not self._player_name and not self._offline:
                self._ui.prompt_player_name()
            else:
                if self._menu:
                    self._ui.display_main_menu()
                elif self._over:
                    self._ui.display_game_over()
                    if not self._offline:
                        self.save_score()
                elif not self._paused and not self._level_up:
                    self._ui.backdrop_active = False
                    self._background.update()
                    self._player.update(self)
                    self._mob_manager.update(self)
                    pygame.draw.rect(self._screen, "red", (self._world_end.x, self._world_end.y, self._world_width, self._world_height), width=5)
                    self._ui.display_game_ui(self)
                    self._timer += 1 / 60

                self._audio_manager.update()
                
            self._ui.display_game_version()
            # flip() the display to put your work on screen
            pygame.display.flip()
            self._dt = self._clock.tick(60) / 1000


        pygame.quit()

    def set_name(self, name):
        self._player_name = name
        if not self._offline:
            self._firestore.create_session(name)

    def save_score(self):
        if not self._scored_saved:
            self._firestore.save_score(self._player_name, self._mob_manager.dead_mobs_count, self._timer, self._player.level)
            self._scored_saved = True

    def pause(self):
        self._paused = not self._paused
        self._ui.pop_up("paused", width=550)
        self._ui.display_tips()
        self._ui.display_controls()

    def restart(self):
        self.start()