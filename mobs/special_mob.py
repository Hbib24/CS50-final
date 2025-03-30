import pygame
from mobs.basic_mob import BasicMob


class SpecialMob(BasicMob):
    def __init__(self, game):
        super().__init__(game, max_health=500, sprites_path="assets/skeleton", scale_factor=2)