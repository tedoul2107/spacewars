import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.velocity = 14
        self.image = pygame.image.load('./assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 20
        self.rect.y = player.rect.y - 15

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.y -= self.velocity
        #verifier si notre projectile n'est plus présent su l'écran
        if self.rect.y < -10:
            self.remove()
        #si le projectile entre en collision avec le monstre
        for monster in self.player.game.ckeck_collision(self, self.player.game.all_monsters):
            #supprimer le projectile
            self.remove()
            #infliger des degats
            monster.damage(self.player.attack)
        for monster in self.player.game.ckeck_collision(self, self.player.game.all_aliens):
            #supprimer le projectile
            self.remove()
            #infliger des degats
            monster.damage(self.player.attack)
