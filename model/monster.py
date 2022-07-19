import pygame
import random
from model.missile import Missile
random.seed(1)

class Monster(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 2
        self.image = pygame.image.load(f'./assets/monster{self.game.niveau}.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1000)
        self.rect.y = random.randint(-500, -100)
        self.position_y = random.randint(-5, 200)
        self.velocity = random.randint(4, 8) + self.game.difficulty/2
        self.tir = 0
        self.all_missiles = pygame.sprite.Group()
        self.mouv = random.randint(0, 1)


    def tir_missile(self):
        if self.tir < 600:
            self.tir += self.velocity
        else:
            self.launch_missile()
            self.tir = 0

    def forward(self):
        if self.rect.y <= self.position_y:
            self.rect.y += self.velocity
        #si le monstre est en collision avec le joueur
        if self.game.ckeck_collision(self, self.game.all_players):
            #infliger des degats au joueur
            self.game.player.damage(self.attack)

        # faire bouger le monstre de gauche a droite
        if self.mouv == 0:
            self.rect.x -= self.velocity
        elif self.mouv == 1:
            self.rect.x += self.velocity
        if self.rect.x <= 0:
            self.mouv = 1
        elif self.rect.x >= 1000:
                self.mouv = 0


    def update_health_bar(self, surface):
        #definir une couleur pour notre jauge de vie
        bar_color = (0, 100, 100)
        #couleur de l'arriere plan de la jauge
        back_bar_color = (60, 63, 60)

        #definir la position de la jauge de vie et ses dimensions
        bar_position = [self.rect.x, self.rect.y, self.health, 5]
        #position de l'arriere plan de la jauge
        back_bar_position = [self.rect.x, self.rect.y, self.max_health, 5]

        #dessiner l'arriere jauge de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        #dessiner la barre de vie
        pygame.draw.rect(surface, bar_color, bar_position)


    def damage(self, amount):
        #infliger les degats
        self.health -= amount
        #verifier que le monstre est encore en vie
        if self.health <= 0:
            # reapparaitre comme un nouveau monstre
            self.position_y = random.randint(-5, 200)
            self.rect.x = self.rect.x
            self.rect.y = random.randint(-500, -100)
            self.velocity = random.randint(4, 8)
            self.health = self.max_health
            # ajouter les points au score
            self.game.add_score(100)

            self.game.sound_manager.play('boom')

            #si la barre est chargée à son maximum
            if self.game.comet_event.is_full_loaded_comet():
                #retirer le monstre du jeu
                self.game.all_monsters.remove(self)
                # appel de la methode pour essayer de declencher la pluie de meteorite
                self.game.comet_event.attempt_fall()
                # self.game.comet_event.boss_fall()


    def launch_missile(self):
        #creer une nouvelle instance de projectile
        missile = Missile(self, self.game, self.rect.x + 25, self.rect.y + 85)
        self.all_missiles.add(missile)


class Alien(Monster):

    def __init__(self, game):
        self.game = game
        super().__init__(game)
        self.image = pygame.image.load(f'./assets/alien{game.niveau}.png')
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.health = 2000 + self.game.difficulty * 1000 * 2
        self.max_health = 2000 + self.game.difficulty * 1000 * 2
        self.attack = 200
        self.rect.y = random.randint(-500, -100)
        self.position_y = random.randint(-5, 50)
        self.mouv = random.randint(0, 1)
        self.velocity = 8 + self.game.difficulty
        self.velocity2 = self.velocity + 1

    def launch_missile(self):
        #creer une nouvelle instance de projectile
        for i in range(6 + 2 * self.game.difficulty):
            missile = Missile(self, self.game, self.rect.x + random.randint(-200, 350), self.rect.y + random.randint(0, 100))
            self.all_missiles.add(missile)

    def tir_missile(self):
        if self.health > self.max_health * 0.5 :
            if self.tir < 370:
                self.tir += self.velocity
            else:
                self.launch_missile()
                self.tir = 0
        else:
            self.velocity = self.velocity2
            if self.tir < 300 + self.velocity * 20:
                self.tir += self.velocity
            else:
                self.launch_missile()
                self.tir = 0


    def forward(self):
        if self.rect.y <= self.position_y:
            self.rect.y += self.velocity
        #si le monstre est en collision avec le joueur
        if self.game.ckeck_collision(self, self.game.all_players):
            #infliger des degats au joueur
            self.game.player.damage(self.attack)
        #faire bouger le monstre de gauche a droite
        if self.mouv == 0 :
            self.rect.x -= self.velocity
        elif self.mouv == 1 :
            self.rect.x += self.velocity
        if self.rect.x <= 0:
            self.mouv = 1
        elif self.rect.x >= 850:
            self.mouv = 0

    def update_health_bar(self, surface):
        #definir une couleur pour notre jauge de vie
        bar_color = (0, 100, 100)
        #couleur de l'arriere plan de la jauge
        back_bar_color = (0, 0, 0)

        #definir la position de la jauge de vie et ses dimensions
        bar_position = [self.rect.x - 25, self.rect.y, self.health * (350 / (self.max_health)), 5]
        #position de l'arriere plan de la jauge
        back_bar_position = [self.rect.x -25, self.rect.y, self.max_health * (350 / (self.max_health)), 5]

        #dessiner l'arriere jauge de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        #dessiner la barre de vie
        pygame.draw.rect(surface, bar_color, bar_position)


    def damage(self, amount):
        #infliger les degats
        self.health -= amount
        #verifier que le monstre est encore en vie
        if self.health <= 0:
            # reapparaitre comme un nouveau monstre
            self.position_y = random.randint(0, 50)
            self.rect.x = random.randint(0, 850)
            self.rect.y = random.randint(-500, -100)
            self.velocity = 4 + self.game.difficulty
            self.health = self.max_health
            #ajouter les points au score
            self.game.add_score(1000)

            self.game.sound_manager.play('boom2')

            # si la barre est chargée à son maximum
            if self.game.comet_event.is_full_loaded_boss():
                # retirer le monstre du jeu
                self.game.all_aliens.remove(self)
                # appel de la methode pour essayer de declencher la pluie de meteorite
                # self.game.comet_event.attempt_fall()
                # self.game.comet_event.boss_fall()

                # remettre la barre à 0
                self.game.comet_event.reset_percent_boss()
                # apparaitre les monstres
                # self.game.comet_event.game.start()
                self.game.spawn_monster()

