from attack import Attack
from unit import Unit

class ProximityAttack(Attack):
    def __init__(self, owner: Unit, target: Unit, cooldown=500, damage=10):
        super().__init__(owner, target, cooldown, damage)

    def trigger(self, screen):
        if self.owner.collides_with(self.target.hitbox):
            self.target.take_damage(self.damage)