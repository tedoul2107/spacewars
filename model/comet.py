import pygame
import random

class Comet(pygame.sprite.Sprite):

    def __init__(self, comet_event):
        super().__init__()
        self.comet_event = comet_event
        self.image = pygame.image.load(f'./assets/comet{self.comet_event.game.niveau}.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.velocity = random.randint(6, 10) + self.comet_event.game.difficulty * 2
        self.rect.x = random.randint(0, 1000)
        self.rect.y = random.randint(-500, -100)
        self.attack = 200

    def remove(self):
        self.comet_event.all_comets.remove(self)
        #verifier si le nombre de comet est 0
        if len(self.comet_event.all_comets) == 0:
            self.comet_event.boss_fall()
            #remettre la barre à 0
            # self.comet_event.reset_percent_boss()
            #apparaitre les monstres
            # self.comet_event.game.start()

    def fall(self):
        self.rect.y += self.velocity
        if self.rect.y > 720:
            # print('del')
            self.remove()

            #si il n'y a plus de boule de feu
            if len(self.comet_event.all_comets) == 0:
                #remettre la jauge au depart
                # self.comet_event.boss_fall()
                self.comet_event.fall_mode = False
        else:
            self.comet_event.game.sound_manager.play('meteorite')

        #verifier si la boule de feu touche le joueur
        if self.comet_event.game.ckeck_collision(self, self.comet_event.game.all_players):
            #retirer la boule de feu
            self.remove()
            #subir les degats
            self.comet_event.game.player.damage(self.attack)
            if self.comet_event.game.player.health > self.comet_event.game.player.max_health:
                self.comet_event.game.player.health = self.comet_event.game.player.max_health


class Health(Comet):

    def __init__(self, comet_event):
        super().__init__(comet_event)
        self.image = pygame.image.load('./assets/health.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.velocity = random.randint(4, 8) + self.comet_event.game.difficulty * 2
        self.attack = -400


    def remove(self):
        self.comet_event.all_healths.remove(self)