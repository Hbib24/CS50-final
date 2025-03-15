from attacks.attack import Attack
from unit import Unit

class ProximityAttack(Attack):
    def __init__(self, owner: Unit, targets: list, duration=500):
        super().__init__(owner, targets, duration)

    def update(self, game):
        if self.can_attack():
            for target in self.targets:
                if self.owner.hitbox.colliderect(target.hitbox):
                    target.take_damage(self.damage)