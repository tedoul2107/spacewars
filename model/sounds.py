import pygame

class SoundManager:

    def __init__(self):
        self.sounds = {
            'click' : pygame.mixer.Sound('./assets/sounds/click.ogg'),
            'boom': pygame.mixer.Sound('./assets/sounds/boom.ogg'),
            'game_over': pygame.mixer.Sound('./assets/sounds/game_over.ogg'),
            'meteorite': pygame.mixer.Sound('./assets/sounds/meteorite.ogg'),
            'musique': pygame.mixer.Sound('./assets/sounds/musique.ogg'),
            'tir': pygame.mixer.Sound('./assets/sounds/tir.ogg'),
            'demarrage': pygame.mixer.Sound('./assets/sounds/demarrage.ogg'),
            'boom2': pygame.mixer.Sound('./assets/sounds/boom2.ogg'),
        }

    def play(self, name, infinie=0, fade=100):
        self.sounds[name].play(loops=infinie, maxtime=0, fade_ms=fade)

    def stop(self, name):
        self.sounds[name].stop()