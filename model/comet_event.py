import pygame
from model.comet import Comet, Health

class CometFallEvent:

    def __init__(self, game):
        self.percent_comet = 0
        self.percent_boss = 0
        self.game = game
        #definir un groupe de sprite pour les comets
        self.all_comets = pygame.sprite.Group()
        self.all_healths = pygame.sprite.Group()
        # self.control_comet = 1
        self.fall_mode = False
        self.boss_mode = False


    def add_percent(self):
        self.percent_comet += 0.03 - self.game.difficulty * 0.003
        # self.percent_boss += 0.1

    def add_percent_boss(self):
        self.percent_boss += 0.7


    def is_full_loaded_comet(self):
        return self.percent_comet >= 100

    def reset_percent_comet(self):
        # if self.percent_boss >= 100:
        if self.game.niveau < 5:
            self.game.niveau += 1
        else:
            self.game.niveau = 1
        self.game.difficulty += 1
        print(self.game.difficulty)
        self.percent_comet = 0


    def is_full_loaded_boss(self):
        return self.percent_boss >= 100

    def reset_percent_boss(self):
        self.percent_boss = 0
        self.reset_percent_comet()


    def meteor_fall(self):
        #faire apparaitre les boules de feu
        for i in range(15 + self.game.difficulty):
            self.all_comets.add(Comet(self))


    def health_fall(self):
        self.all_healths.add(Health(self))


    def attempt_fall(self):
        #la jauge d'evenement est totalement chargée
        if self.is_full_loaded_comet() and len(self.game.all_monsters) == 0:
            print("pluie de meteorite")
            self.meteor_fall()
            self.health_fall()
            self.fall_mode = True
            # self.game.sound_manager.play('meteorite')
            # if self.is_full_loaded_boss() and len(self.all_comets) == 0:
            # self.boss_fall()
            # self.game.spawn_alien()
            # self.control_comet = 2


    def boss_fall(self):
        #la jauge d'evenement est totalement chargée
        if self.is_full_loaded_boss() and len(self.all_comets) == 0:
            print("pluie de boss")
            self.game.spawn_alien()
            self.boss_mode = True
            # self.reset_percent_boss()


    def update_bar(self, surface):
        #ajouter du pourcentage a la barre
        self.add_percent()
        if self.fall_mode:
            self.add_percent_boss()

        # appel de la methode pour essayer de declencher le boss
        # self.boss_fall()

        #bar noir en arriere plan
        pygame.draw.rect(surface, (0, 0, 0), [
            0, #axe des x
            surface.get_height() - 6, #axe des y
            surface.get_width(), #longueur
            6
        ])
        #bar bleue pour les comets
        pygame.draw.rect(surface, (0, 100, 200), [
            0,  # axe des x
            surface.get_height() - 6,  # axe des y
            (surface.get_width() / 100) * self.percent_comet,  # longueur
            6
        ])
        #bar rouge pour le boss
        pygame.draw.rect(surface, (187, 11, 11), [
            0,  # axe des x
            surface.get_height() - 6,  # axe des y
            (surface.get_width() / 100) * self.percent_boss,  # longueur
            6
        ])