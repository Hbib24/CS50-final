import enum
import pygame

class Event(enum.Enum):
    MOB_KILL = pygame.USEREVENT + 1
    LEVEL_UP = pygame.USEREVENT + 2
    ABILITY_PICK = pygame.USEREVENT + 3
    PLAYER_MOVE = pygame.USEREVENT + 4
    MOB_HIT = pygame.USEREVENT + 5
    PLAYER_HIT = pygame.USEREVENT + 6
    MOUSE_CLICK = pygame.USEREVENT + 7
    KB_DOWN = pygame.USEREVENT + 8

class EventManager:
    def __init__(self):
        self.listeners = {}

    def post_event(self, event: Event, data=None):
        pygame.event.post(pygame.event.Event(event.value, data=data or {}))

    def listen_to(self, event: Event, callback):
        if event.value not in self.listeners:
            self.listeners[event.value] = []
        self.listeners[event.value].append(callback)

    def handle_event(self, event):
        for event_type, callbacks in self.listeners.items():
            if event.type == event_type:
                for callback in callbacks:
                    callback(event)
