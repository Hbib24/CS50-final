from unit import Unit

import pygame

def test_movement():
    unit = Unit((320, 240), "assets/player/player.png")
    
    assert unit.get_pos().x == pygame.Vector2((320, 240)).x
    assert unit.get_pos().y == pygame.Vector2((320, 240)).y