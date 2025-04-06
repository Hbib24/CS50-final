import pygame

from src.event_manager import Event


class AudioManager():
    DIR = "assets/audio/"

    def __init__(self, game):
        level_up = pygame.mixer.Sound(f"{self.DIR}level_up.wav")
        mob_hit = pygame.mixer.Sound(f"{self.DIR}mob_hit.wav")
        player_hit = pygame.mixer.Sound(f"{self.DIR}player_hit.wav")

        self.last_played_at = 0
        
        game._event_manager.listen_to(Event.LEVEL_UP, lambda _: self.play_sound(level_up))
        game._event_manager.listen_to(Event.MOB_HIT, lambda _: self.play_sound(mob_hit, 500))
        game._event_manager.listen_to(Event.PLAYER_HIT, lambda _: self.play_sound(player_hit, 500))

    def play_sound(self, sound: pygame.mixer.Sound, cooldown = 0):
        time = pygame.time.get_ticks()

        if self.last_played_at + cooldown <= time:
            sound.set_volume(0.5)
            sound.play()
            self.last_played_at = time
