import pygame


class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.backdrop_active = False
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = pygame.font.FontType("assets/ui/monogram.ttf", 35)

        self.time_icon = pygame.image.load("assets/ui/icon_time.png").convert_alpha()
        self.time_icon = pygame.transform.smoothscale(self.time_icon, (35, 35))

        self.skull_icon = pygame.image.load("assets/ui/icon_skull.png").convert_alpha()
        self.skull_icon = pygame.transform.smoothscale(self.skull_icon, (35, 35))

        self.heart_icon = pygame.image.load("assets/ui/icon_heart.png").convert_alpha()
        self.heart_icon = pygame.transform.smoothscale(self.heart_icon, (35, 35))

    def display_game_ui(self, game):
        # health
        self.screen.blit(self.heart_icon, (20, 20))
        pygame.draw.rect(self.screen, (40, 40, 40), (60 - 3, 25 - 3, 206, 26), border_radius=5) 
        pygame.draw.rect(self.screen, (80, 80, 80), (60, 25, 200, 20), border_radius=5) 

        hp_percentage = game._player.health / game._player._max_health
        current_hp_width = int(200 * hp_percentage)
        hp = self.font.render(f"{game._player.health}/{game._player._max_health}", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 200, 0), (60, 25, current_hp_width, 20), border_radius=5)
        self.screen.blit(hp, (65, 19))

        self.display_score(game._mob_manager.dead_mobs_count, (self.screen_width - 245, 20), game)
        self.display_time((self.screen_width - 145, 20))
        self.display_level(game)
        
    def backdrop(self):
        if not self.backdrop_active:
            surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            pygame.draw.rect(surface, (50, 50, 50, 70), (0, 0, self.screen_width, self.screen_height))
            self.screen.blit(surface, (0, 0))
            self.backdrop_active = True
        
    def pop_up(self, title, content, width=400, height=350):
        self.backdrop()
        
        center = (self.screen_width // 2, self.screen_height // 2)
        pygame.draw.rect(self.screen, (40, 40, 40),(center[0] - width // 2 - 3, center[1] - height // 2 - 3, width + 6, height + 6), border_radius=5)
        pygame.draw.rect(self.screen, (80, 80, 80),(center[0] - width // 2, center[1] - height // 2, width, height), border_radius=5)
        title = self.font.render(f"{title.title()}", True, (255, 255, 255))
        
        self.screen.blit(title, (center[0] - (title.get_width() // 2), center[1] - height // 2 + 20))
        
    def display_score(self, score, pos: tuple, game):
        score = self.font.render(f"{score}", True, (255, 255, 255))
        self.screen.blit(self.skull_icon, pos)
        self.screen.blit(score, (pos[0] + 45, pos[1]))

    def display_time(self, pos: tuple):
        elapsed_time = pygame.time.get_ticks() // 1000
        time = self.font.render(f"{self.get_formatted_time(elapsed_time)}", True, (255, 255, 255))

        self.screen.blit(self.time_icon, pos)
        self.screen.blit(time, (pos[0] + 45, pos[1]))

    def display_level(self, game):
        level = self.font.render(f"Level: {game._player.level}", True, (255, 255, 255))
        x = (self.screen_width // 2)-200
        y = self.screen_height - 35
        pygame.draw.rect(self.screen, (40, 40, 40), (x - 3, y - 3, 406, 36), border_radius=5) 
        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, 400, 30), border_radius=5) 
        
        xp_per = game._player.experience / game._player.levelup_experience
        current_xp_width = int(400 * xp_per)
        pygame.draw.rect(self.screen, (255, 200, 0), (x, y, current_xp_width, 30), border_radius=5)
        
        self.screen.blit(level, ((self.screen_width // 2) - (level.get_width() // 2), y))

    def get_formatted_time(self, time):
        minutes = int(time // 60)
        seconds = int(time % 60)

        return f'{minutes:02}:{seconds:02}'