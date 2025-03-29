import pygame
from mobs.basic_mob import BasicMob


class SpecialMob(BasicMob):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        super().__init__(screen, max_health=500, sprites_path="assets/skeleton", scale_factor=2, speed=1.6)