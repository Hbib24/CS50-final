import pygame

from src.event_manager import Event

class Button:
    def __init__(self, game, text, callback, rect = (0, 0, 0, 0), bg_color = (80, 80, 80)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.FontType("assets/ui/monogram.ttf", 35)
        self.bg_color = bg_color
        self.callback = callback  # Function to call when clicked

        # Render text once


        game._event_manager.listen_to(Event.MOUSE_CLICK, self.handle_event)

    def draw(self, surface):
        pygame.draw.rect(surface, (40, 40, 40), self.rect.inflate(6, 6), border_radius=5)
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=5)

        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, self.text_rect)

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)
        return self
        
    def handle_event(self, event):
        if self.rect.collidepoint(event.data.pos):
            self.callback()
