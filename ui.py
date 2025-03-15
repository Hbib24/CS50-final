import pygame

class UI:
    def __init__(self):
        self.time_icon = pygame.image.load("assets/ui/icon_time.png").convert_alpha()
        self.time_icon = pygame.transform.smoothscale(self.time_icon, (30, 30))

        self.skull_icon = pygame.image.load("assets/ui/icon_skull.png").convert_alpha()
        self.skull_icon = pygame.transform.smoothscale(self.skull_icon, (30, 30))

        self.heart_icon = pygame.image.load("assets/ui/icon_heart.png").convert_alpha()
        self.heart_icon = pygame.transform.smoothscale(self.heart_icon, (30, 30))

        self.font = pygame.font.FontType(None, 32)

    def display_game_ui(self, game):
        screen: pygame.Surface = game._screen
        screen_width = screen.get_width()

        # health
        screen.blit(self.heart_icon, (20, 20))
        pygame.draw.rect(screen, (50, 50, 50), (60, 25, 200, 20)) 

        hp_percentage = game._player.health / game._player._max_health
        current_hp_width = int(200 * hp_percentage)
        pygame.draw.rect(screen, (0, 200, 0), (60, 25, current_hp_width, 20))

        # score
        score = self.font.render(f"{game._score}", True, (255, 255, 255))
        screen.blit(self.skull_icon, (screen_width - 150, 20))
        screen.blit(score, (screen_width - 110, 25))

        # time
        elapsed_time = pygame.time.get_ticks() // 1000
        time = self.font.render(f"{elapsed_time}", True, (255, 255, 255))
        screen.blit(self.time_icon, (screen_width - 70, 20))
        screen.blit(time, (screen_width - 40, 25))