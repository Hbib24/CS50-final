import pygame


class UI:
    def __init__(self, screen, player):
        self._screen = screen
        self._player = player
        self._font = pygame.font.SysFont('Arial', 30)

    def display_game_over(self, timer, score):
        font = pygame.font.SysFont('Arial', 50)
        game_over_text = font.render('GAME OVER', True, (255, 0, 0))
        time_text = font.render(f"Time: {self.get_formatted_timer(timer)}", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        restart_text = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))

        self._screen.fill((0, 0, 0))  # Fill screen with black to show game over
        self._screen.blit(game_over_text, (self._screen.get_width() // 2 - game_over_text.get_width() // 2, self._screen.get_height() // 2 - 100))
        self._screen.blit(score_text, (self._screen.get_width() // 2, self._screen.get_height() // 2 + 50))
        self._screen.blit(time_text, (self._screen.get_width() // 2 - 300, self._screen.get_height() // 2 + 50))
        self._screen.blit(restart_text, (self._screen.get_width() // 2 - restart_text.get_width() // 2, self._screen.get_height() // 2 + 150))



    def draw(self, timer, level, score):
        health_percentage = self._player._current_health / self._player._max_health
        health_width = 200
        health_height = 20
        pygame.draw.rect(self._screen, (0, 0, 0), (20, 20, health_width, health_height)) 
        pygame.draw.rect(self._screen, (0, 150, 0), (20, 20, health_width * health_percentage, health_height)) 
        

        health_text = self._font.render(f'{self._player._current_health}/{self._player._max_health}', True, (255, 255, 255))
        self._screen.blit(health_text, (20, 50))


        timer_text = self._font.render(self.get_formatted_timer(timer), True, (255, 255, 255))
        self._screen.blit(timer_text, (self._screen.get_width() - 100, 20)) 


        level_text = self._font.render(f"Level: {level}", True, (255, 255, 255))
        self._screen.blit(level_text, (self._screen.get_width() - 250, 20)) 

        score_text = self._font.render(f"Score: {score}", True, (255, 255, 255))
        self._screen.blit(score_text, (self._screen.get_width() - 400, 20)) 
        
    def display_pause_menu(self):
        font = pygame.font.SysFont('Arial', 50)
        pause_text = font.render('Game Paused', True, (255, 0, 0))
        restart_text = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))

        self._screen.fill((0, 0, 0)) 
        self._screen.blit(pause_text, (self._screen.get_width() // 2 - pause_text.get_width() // 2, self._screen.get_height() // 2 - 100))
        self._screen.blit(restart_text, (self._screen.get_width() // 2 - restart_text.get_width() // 2, self._screen.get_height() // 2 + 50))

    def get_formatted_timer(self, timer):
        minutes = int(timer // 60)
        seconds = int(timer % 60)

        return f'{minutes:02}:{seconds:02}'