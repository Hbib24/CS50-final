import enum
from attacks.sword_attack import SwordAttack
from event_manager import Event

class Ability(enum.Enum):
    HEAL = "heal"
    SPEED = "speed"
    SWD_DMG = "swd_dmg"
    SWD_CD = "swd_cd"
    SWD_DUR = "swd_dur"

class AbilityManager:
    def __init__(self, game):
        self.game = game

        game._player.add_attack(SwordAttack(game._player, []))
        game._event_manager.listen_to(Event.ABILITY_PICK, self.pick_ability)

    def pick_ability(self, ability):
        ability_id = ability.data.get("id")
        match ability_id:
            case Ability.HEAL.value:
                self.game._player.heal(20)
            case Ability.SPEED.value:
                self.game._player._speed += self.game._player._speed * 0.02
            case Ability.SWD_DMG.value:
                attack = self.game._player.find_attack(lambda attack: isinstance(attack, SwordAttack))
                attack.damage += attack.damage * 0.02
            case Ability.SWD_CD.value:
                attack = self.game._player.find_attack(lambda attack: isinstance(attack, SwordAttack))
                attack.cooldown -= attack.cooldown * 0.02
            case Ability.SWD_CD.value:
                attack = self.game._player.find_attack(lambda attack: isinstance(attack, SwordAttack))
                attack.duration -= attack.duration * 0.02
