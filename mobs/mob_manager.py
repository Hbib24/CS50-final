from mobs.basic_mob import BasicMob

class MobManager:
    def __init__(self):
        self.mobs = []
        self.spawn_cooldown = 300

    def spawn_basics(self):
        while True:
            mob = BasicMob()