from unit import Unit

class Attack():
    def __init__(self, owner: Unit, targets: tuple, cooldown=1000, damage=10, duration=500):
        self.cooldown = cooldown
        self.damage = damage
        self.duration = duration
        self.targets = targets
        self.owner = owner
        self.last_attack_time = 0

