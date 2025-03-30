import random
import pygame
from attacks.proximity_attack import ProximityAttack
from event_manager import Event
from mobs.basic_mob import BasicMob
from mobs.special_mob import SpecialMob

class MobManager:
    def __init__(self):
        self.active_mobs = []
        self.dead_mobs_count = 0
        self.next_spawn_time = 0
        self.next_special_spawn_time = 60000

    def spawn(self, type, game):
        match type:
            case "basic":
                mob = BasicMob(game)
            case "special":
                mob = SpecialMob(game)

        mob.add_attack(ProximityAttack(mob, [game._player]))
        self.active_mobs.append({"instance": mob, "type": type})

        for attack in game._player._attacks:
                attack.add_target(mob)

    def update(self, game):
        timer = pygame.time.get_ticks()
        min_interval = 1000
        max_interval = 3000
        if game._player.level > 5:
            min_interval = 800
            max_interval = 1200
        elif game._player.level > 10:
            min_interval = 500
            max_interval = 1000
            
        random_interval = random.randint(min_interval, max_interval) 

        if timer >= self.next_spawn_time:
            self.spawn("basic", game)
            self.next_spawn_time = timer + random_interval
        
        if timer >= self.next_special_spawn_time:
            self.spawn("special", game)
            self.next_special_spawn_time = timer + random.randint(30000, 50000)

        for i, mob in reversed(list(enumerate(self.active_mobs))):
            instance = mob.get("instance")
            if instance.is_dead:
                self.active_mobs.pop(i)
                self.dead_mobs_count += 1
                game._event_manager.post_event(Event.MOB_KILL, mob)
                pass

            instance.update(game)
