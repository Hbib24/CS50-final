import pygame

from event_manager import Event

class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.time_icon = pygame.image.load("assets/ui/icon_time.png").convert_alpha()
        self.time_icon = pygame.transform.smoothscale(self.time_icon, (35, 35))

        self.skull_icon = pygame.image.load("assets/ui/icon_skull.png").convert_alpha()
        self.skull_icon = pygame.transform.smoothscale(self.skull_icon, (35, 35))

        self.heart_icon = pygame.image.load("assets/ui/icon_heart.png").convert_alpha()
        self.heart_icon = pygame.transform.smoothscale(self.heart_icon, (35, 35))

        self.font = pygame.font.FontType("assets/ui/monogram.ttf", 35)

        game._event_manager.listen_to(Event.MOB_KILL, self.on_mob_kill)

    def display_game_ui(self, game):
        # health
        self.screen.blit(self.heart_icon, (20, 20))
        pygame.draw.rect(self.screen, (50, 50, 50), (60, 25, 200, 20), border_radius=5) 

        hp_percentage = game._player.health / game._player._max_health
        current_hp_width = int(200 * hp_percentage)
        hp = self.font.render(f"{game._player.health}", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 200, 0), (60, 25, current_hp_width, 20), border_radius=5)
        self.screen.blit(hp, (65, 19))

        self.display_score(game._mob_manager.dead_mobs_count, (self.screen_width - 245, 20), game)
        self.display_time((self.screen_width - 145, 20))
        self.display_level(game._player.level)


    def display_score(self, score, pos: tuple, game):
        score = self.font.render(f"{score}", True, (255, 255, 255))
        self.screen.blit(self.skull_icon, pos)
        self.screen.blit(score, (pos[0] + 45, pos[1]))


    def display_time(self, pos: tuple):
        elapsed_time = pygame.time.get_ticks() // 1000
        time = self.font.render(f"{self.get_formatted_time(elapsed_time)}", True, (255, 255, 255))

        self.screen.blit(self.time_icon, pos)
        self.screen.blit(time, (pos[0] + 45, pos[1]))

    def display_level(self, level):
        level = self.font.render(f"Level: {level}", True, (255, 255, 255))
        x = (self.screen_width // 2)-200
        y = self.screen_height - 35
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, 400, 30), border_radius=5) 
        self.screen.blit(level, ((self.screen_width // 2) - (level.get_width() // 2), y))

    def on_mob_kill(self, _):
        self.skull_icon = pygame.transform.smoothscale(self.skull_icon, (40, 40))

    def get_formatted_time(self, time):
        minutes = int(time // 60)
        seconds = int(time % 60)

        return f'{minutes:02}:{seconds:02}'