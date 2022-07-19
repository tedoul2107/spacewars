import pygame

class Missile(pygame.sprite.Sprite):

    def __init__(self, monster, game, x, y):
        super().__init__()
        self.game = game
        self.monster = monster
        self.velocity = 4 + self.game.difficulty * 2
        self.image = pygame.image.load(f'assets/missile{self.game.niveau}.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.origin_image = self.image
        self.angle = 0
        self.attack = 100 + self.game.difficulty * 10

    def rotate(self):
        self.angle += 10
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center = self.rect.center)

    def remove(self):
        self.monster.all_missiles.remove(self)

    def move(self):
        self.rect.y += self.velocity
        if self.game.niveau == 1:
            self.rotate()
        #verifier si notre projectile n'est plus présent su l'écran
        if self.rect.y > 720:
            self.remove()
        #verifier que le projectile est en collision avec le joueur
        if self.game.ckeck_collision(self, self.game.all_players):
            self.remove()
            self.game.player.damage(self.attack)

        #si le projectile entre en collision avec le monstre
        # for monster in self.player.game.ckeck_collision(self, self.player.game.all_monsters):
        #     #supprimer le projectile
        #     self.remove()
        #     #infliger des degats
        #     monster.damage(self.player.attack)