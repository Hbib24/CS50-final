import pygame
import pytest 
from src.attacks.area_attack import AreaAttack
from src.attacks.rotating_attack import RotatingAttack
from src.ability_manager import Abilities, PowerUps
from src.attacks.sword_attack import SwordAttack
from src.event_manager import Event, EventManager
from src.mobs.mob_manager import MobManager
from src.game import Game 
from src.player import Player
from src.audio_manager import AudioManager

def test_game_initialization():
    game = Game(offline=True)

    assert isinstance(game, Game)
    assert isinstance(game._event_manager, EventManager)
    assert isinstance(game._player, Player)
    assert isinstance(game._mob_manager, MobManager)
    assert isinstance(game._audio_manager, AudioManager)
    assert pygame.get_init() is True
    assert game._firestore is None
    assert game._running is True
    assert game._menu is True
    
def test_movement():
    game = Game(offline=True)

    pos = (game._screen.get_width() // 2, game._screen.get_height() // 2) # center of the screen
    speed = game._player._speed
    assert game._player.simulated_position == pygame.Vector2(pos)

    game._player.simulate_movement(1, 0)
    assert game._player.simulated_position == pygame.Vector2(pos[0] + 1 * speed, pos[1])

    game._player.simulate_movement(-22, 0)
    assert game._player.simulated_position == pygame.Vector2(pos[0] - 21 * speed, pos[1])

    game._player.simulate_movement(0, 1)
    assert game._player.simulated_position == pygame.Vector2(game._player.simulated_position.x, pos[1] + 1 * speed)

    game._player.simulate_movement(0, -12)
    assert game._player.simulated_position == pygame.Vector2(game._player.simulated_position.x, pos[1] - 11 * speed)

    game._player.simulate_movement(1, 1)
    assert game._player.simulated_position == pygame.Vector2(pos[0] - 20 * speed, pos[1] - 10 * speed)

    game._player.simulate_movement(0, 2000)
    assert game._player.is_out_of_bounds(game._player.simulated_position.x, game._player.simulated_position.y) is True

    game._player.simulate_movement(2000, -2000)
    assert game._player.is_out_of_bounds(game._player.simulated_position.x, game._player.simulated_position.y) is True

def test_level_system():
    game = Game(offline=True)
    
    assert game._player.level == 1
    assert game._player.experience == 0

    game._player.gain_experience(pygame.event.Event(Event.MOB_KILL.value, data=dict(type="basic")))
    assert game._player.experience == 20
    assert game._player.level == 1

    game._player.gain_experience(pygame.event.Event(Event.MOB_KILL.value, data=dict(type="special")))
    assert game._player.experience == 70
    assert game._player.level == 1

    game._player.gain_experience(pygame.event.Event(Event.MOB_KILL.value, data=dict(type="special")))
    assert game._player.experience == 20 # after level up, the experience is reset
    assert game._player.level == 2

def test_abilities():
    game = Game(offline=True)

    powers = game._ability_manager.get_random_powers()
    assert len(powers) == 3

    abilities = game._ability_manager._abilities
    game._ability_manager.pick_ability(pygame.event.Event(Event.ABILITY_PICK.value, data=dict(abilities[0])))
    assert game._player.has_attack(lambda attack: isinstance(attack, AreaAttack)) is True

    game._ability_manager.pick_ability(pygame.event.Event(Event.ABILITY_PICK.value, data=dict(abilities[1])))
    assert game._player.has_attack(lambda attack: isinstance(attack, RotatingAttack)) is True