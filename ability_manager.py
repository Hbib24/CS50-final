import enum
import json
import random

import pygame
from attacks.rotating_attack import RotatingAttack
from attacks.sword_attack import SwordAttack
from event_manager import Event

class PowerUps(enum.Enum):
    HEAL = "heal"
    SPEED = "speed"
    SWD_DMG = "swd_dmg"
    SWD_CD = "swd_cd"
    SWD_DUR = "swd_dur"

class Abilities(enum.Enum):
    AOE = "aoe"
    SHURIKEN = "shuriken"

class AbilityManager:
    def __init__(self, game):
        self.game = game
        self.rand_powers = []
        self._power_ups: list = self.get_power_ups()
        self._abilities: list = self.get_abilities()

        game._player.add_attack(SwordAttack(game._player, []))
        game._event_manager.listen_to(Event.ABILITY_PICK, self.pick_ability)

    def pick_ability(self, ability):
        ability_id = ability.data.get("id")
        match ability_id:
            case PowerUps.HEAL.value:
                self.game._player.heal(20)
            case PowerUps.SPEED.value:
                self.game._player._speed += self.game._player._speed * 0.02
            case PowerUps.SWD_DMG.value:
                attack = self.game._player.find_attack(lambda attack: isinstance(attack, SwordAttack))
                attack.damage += attack.damage * 0.02
            case PowerUps.SWD_CD.value:
                attack = self.game._player.find_attack(lambda attack: isinstance(attack, SwordAttack))
                attack.cooldown -= attack.cooldown * 0.02
            case PowerUps.SWD_CD.value:
                attack = self.game._player.find_attack(lambda attack: isinstance(attack, SwordAttack))
                attack.duration -= attack.duration * 0.02
            case Abilities.SHURIKEN.value:
                self.game._player.add_attack(RotatingAttack(self.game._player, self.game._mob_manager.active_mobs.copy()))

    def on_player_pick(self, key):
        if key == pygame.K_1:
            self.game._event_manager.post_event(Event.ABILITY_PICK, self.rand_powers[0])
            self.game._level_up = False
        elif key == pygame.K_2:
            self.game._event_manager.post_event(Event.ABILITY_PICK, self.rand_powers[1])
            self.game._level_up = False
        elif key == pygame.K_3:
            self.game._event_manager.post_event(Event.ABILITY_PICK, self.rand_powers[2])
            self.game._level_up = False

    def get_random_powers(self):
        choices = []
        power_ups = self.power_ups.copy()

        for _ in range(3):
            pwr = random.choice(power_ups)

            power_ups.pop(power_ups.index(pwr))
            choices.append(pwr)
            
        if self.game._player.level >= 5 and not self.game._player.has_attack(lambda attack: isinstance(attack, RotatingAttack)):
            choices[1] = list(filter(lambda x: x.get("id") == "shuriken", self.abilities))[0]

        return choices
    
    def get_power_ups(self):
        with open("assets/definitions/power_ups.json", "r") as file:
            return json.load(file)
        
    def get_abilities(self):
        with open("assets/definitions/abilities.json", "r") as file:
            return json.load(file)
        
    @property
    def power_ups(self):
        return self._power_ups
    
    @property
    def abilities(self):
        return self._abilities