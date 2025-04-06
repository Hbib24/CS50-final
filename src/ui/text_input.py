from src.event_manager import Event
import pygame


class TextInput:
    def __init__(self, game, label, on_submit, min_length=3, max_length=10, rect = (0, 0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.min_length = min_length
        self.max_length = max_length
        self.value = ""
        self.font = pygame.font.FontType("assets/ui/monogram.ttf", 35)
        self.label = label
        self.on_submit = on_submit

        game._event_manager.listen_to(Event.KB_DOWN, self.handle_event)

    def draw(self, surface):
        pygame.draw.rect(surface, (40, 40, 40), self.rect.inflate(6, 6), border_radius=5)
        pygame.draw.rect(surface, (80, 80, 80), self.rect, border_radius=5)

        label = self.font.render(self.label, True, (255, 255, 255))
        surface.blit(label, (self.rect.x + 10, self.rect.y))

        text = self.font.render(self.value, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, (text_rect.x, text_rect.y + 10))

    def handle_event(self, event):
        key = event.data.key
        if key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        elif key == pygame.K_RETURN:
            self.on_submit(self.value)
        elif len(self.value) < self.max_length:
            unicode = event.data.unicode
            self.value += unicode