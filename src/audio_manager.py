import pygame

from src.event_manager import Event


class AudioManager():
    DIR = "assets/audio/"

    def __init__(self, game):
        level_up = pygame.mixer.Sound(f"{self.DIR}level_up.wav")
        mob_hit = pygame.mixer.Sound(f"{self.DIR}mob_hit.wav")
        player_hit = pygame.mixer.Sound(f"{self.DIR}player_hit.wav")

        self.last_played_at = 0
        self.playing = False
        self.game = game
        
        game._event_manager.listen_to(Event.LEVEL_UP, lambda _: self.play_sound(level_up))
        game._event_manager.listen_to(Event.MOB_HIT, lambda _: self.play_sound(mob_hit, 500))
        game._event_manager.listen_to(Event.PLAYER_HIT, lambda _: self.play_sound(player_hit, 500))

    def play_sound(self, sound: pygame.mixer.Sound, cooldown = 0):
        time = pygame.time.get_ticks()

        if self.last_played_at + cooldown <= time:
            sound.set_volume(0.5)
            sound.play()
            self.last_played_at = time

    def play_menu(self):
        if not self.playing:
            pygame.mixer.music.load(f"{self.DIR}track.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.playing = True

    def play_soundtrack(self):
        if not self.playing:
            pygame.mixer.music.load(f"{self.DIR}track.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            self.playing = True
    
    def stop(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False

    def update(self):
        if self.game._menu:
            self.play_menu()
        else:
            pygame.mixer.music.stop()
            self.playing = False
 