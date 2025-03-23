import random
import pygame
from attacks.proximity_attack import ProximityAttack
from event_manager import Event
from mobs.basic_mob import BasicMob

class MobManager:
    def __init__(self):
        self.active_mobs = []
        self.dead_mobs_count = 0
        self.next_spawn_time = 0

    def update(self, game):
        timer = pygame.time.get_ticks()
        self.random_interval = random.randint(100, 500) + timer

        if timer >= self.next_spawn_time:
            mob = BasicMob(game._screen)
            mob.add_attack(ProximityAttack(mob, [game._player]))
            self.active_mobs.append(mob)

            for attack in game._player._attacks:
                attack.add_target(mob)

            self.next_spawn_time = timer + random.randint(1000, 3000)

        for i, mob in reversed(list(enumerate(self.active_mobs))):
            if mob.is_dead:
                self.active_mobs.pop(i)
                self.dead_mobs_count += 1
                game._event_manager.post_event(Event.MOB_KILL)
                pass

            mob.update(game)
