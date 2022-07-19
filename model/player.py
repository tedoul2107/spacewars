import pygame
from model.projectile import Projectile

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 1000
        self.max_health = 1000
        self.attack = 30
        self.velocity = 10
        self.image = pygame.image.load('./assets/player.png')
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 473
        self.rect.y = 500
        self.all_projectiles = pygame.sprite.Group()

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_up(self):
        #si le joueur n'est pas en collision
        if not self.game.ckeck_collision(self, self.game.all_monsters):
            self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity


    def launch_projectile(self):
        #creer une nouvelle instance de projectile
        projectile1 = Projectile(self)
        projectile2 = Projectile(self)
        projectile2.rect.x += 51.8
        self.all_projectiles.add(projectile1, projectile2)
        self.game.sound_manager.play('tir')


    def update_health_bar(self, surface):
        #definir une couleur pour notre jauge de vie
        bar_color = (0, 100, 7)
        #couleur de l'arriere plan de la jauge
        back_bar_color = (60, 63, 60)

        #definir la position de la jauge de vie et ses dimensions
        bar_position = [self.rect.x, self.rect.y + 105, self.health * 0.1, 5]
        #position de l'arriere plan de la jauge
        back_bar_position = [self.rect.x, self.rect.y + 105, self.max_health * 0.1, 5]

        #dessiner l'arriere jauge de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        #dessiner la barre de vie
        pygame.draw.rect(surface, bar_color, bar_position)


    def damage(self, amount):
        if self.health > 0:
            self.health -= amount
        else:
            #si le joueur n'a plus de point de vie
            self.game.game_over()