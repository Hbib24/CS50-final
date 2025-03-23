import pygame

class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.backdrop_active = False
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = pygame.font.FontType("assets/ui/monogram.ttf", 35)
        self.title_font = pygame.font.FontType("assets/ui/monogram.ttf", 45)

        self.arrow_keys = pygame.image.load("assets/ui/arrow_keys.png").convert_alpha()

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

    def level_up(self, powers):
        center = (self.screen_width // 2, self.screen_height // 2)
        self.backdrop()

        self.pop_up("Level Up!", width=820, height=40, pos=(center[0], center[1] - 230))

        offset = 0
        for i, pwr in enumerate(powers):
            start = center[0] - 300 + offset
            border_color = (40, 40, 40)
            is_ability = pwr.get("type") == "ability"
            if is_ability:
                border_color = (255, 200, 0)
            
            rect = self.pop_up(pwr.get("name"), width=280, pos=(start, center[1]), border_color=border_color)
            self.text(pwr.get("description"), pos=(start - (rect.width // 2) + 20, center[1] - 50))
            self.text(f"Press {i + 1}", pos=(start - 45, center[1] + (rect.height // 2) - 50))

            if is_ability:
                font = pygame.font.FontType("assets/ui/monogram.ttf", 25)
                txt = font.render("New Attack", True, (255, 200, 0))
                self.screen.blit(txt, (center[0] - txt.get_width() // 2, center[1] - 120))

            offset += 300
        
    def pop_up(self, title, width=400, height=350, pos: tuple=None, border_color: tuple=None):
        self.backdrop()
        
        center = (self.screen_width // 2, self.screen_height // 2)
        pos = pos or center
        border_color = border_color or (40, 40, 40)
        pygame.draw.rect(self.screen, border_color,(pos[0] - width // 2 - 3, pos[1] - height // 2 - 3, width + 6, height + 6), border_radius=5)
        rect = pygame.draw.rect(self.screen, (80, 80, 80),(pos[0] - width // 2, pos[1] - height // 2, width, height), border_radius=5)
        title = self.title_font.render(f"{title.title()}", True, (255, 255, 255))
        
        self.screen.blit(title, (pos[0] - (title.get_width() // 2), pos[1] - height // 2 + height * 0.05))
        return rect

    def text(self, str, size=35, pos=None):
        center = (self.screen_width // 2, self.screen_height // 2)
        font = pygame.font.FontType("assets/ui/monogram.ttf", size)
        pos = pos or center

        lines = str.split("\n")
        y = pos[1]
        for line in lines:
            txt = font.render(f"{line}", True, (255, 255, 255))
            self.screen.blit(txt, (pos[0], y))

            y += txt.get_height()
        
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

    def display_tips(self):
        center = (self.screen_width // 2, self.screen_height // 2)
        tip1 = self.font.render(f"Use arrow keys to move", True, (255, 255, 255))
        tip2 = self.font.render(f"Attacks are triggered automatically", True, (255, 255, 255))
        
        self.screen.blit(self.arrow_keys, (center[0] - self.arrow_keys.get_width() // 2, center[1] - self.arrow_keys.get_height() // 2 - 50))
        self.screen.blit(tip1, (center[0] - tip1.get_width() // 2, center[1]))
        self.screen.blit(tip2, (center[0] - tip2.get_width() // 2, center[1] + 30))

    def display_controls(self):
        center = (self.screen_width // 2, self.screen_height // 2)
        tip1 = self.font.render(f"Press R to restart", True, (255, 255, 255))
        tip2 = self.font.render(f"Press Q to quit", True, (255, 255, 255))

        self.screen.blit(tip1, (center[0] - tip1.get_width() // 2, center[1] + 100))
        self.screen.blit(tip2, (center[0] - tip2.get_width() // 2, center[1] + 130))

    def get_formatted_time(self, time):
        minutes = int(time // 60)
        seconds = int(time % 60)

        return f'{minutes:02}:{seconds:02}'