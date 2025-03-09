import random
from mob import Mob

class MobSpawner:
    SPAWN_FREQUENCY_INTERVAL = 30

    def __init__(self, screen, player):
        self._screen = screen
        self._player = player
        self._spawn_timer = 0  # Track elapsed time
        self._spawn_frequency = 10000  # Spawn cooldown
        self._spawn_frequency_interval = self.SPAWN_FREQUENCY_INTERVAL  # Every x seconds, decrease spawn cooldown (increase level)
        self._mobs = []  # List to hold all active mobs

    def spawn_mob(self):
        new_mob = Mob(self._screen, self._player)
        self._mobs.append(new_mob)

    def update(self, dt, increment_level, increment_score, attack_pos=None):
        self._spawn_timer += dt
        self._spawn_frequency_interval -= 1 / 60
        spawn_interval = random.randint(500, self._spawn_frequency)

        if 0 >= self._spawn_frequency_interval and self._spawn_frequency > 1000:
            increment_level()
            self._spawn_frequency -= 100
            self._spawn_frequency_interval = self.SPAWN_FREQUENCY_INTERVAL

        if self._spawn_timer >= spawn_interval:
            self.spawn_mob()
            self._spawn_timer = 0

        if attack_pos:
            for i, mob in enumerate(self._mobs):
                mob.handle_attacked(attack_pos)
                if mob.is_dead:
                    self._mobs.pop(i)
                    increment_score()


    def draw_mobs(self, dt):
        # Update and draw all mobs
        for mob in self._mobs:
            mob.chase_player()
            mob.attack_player(dt)
            mob.draw()