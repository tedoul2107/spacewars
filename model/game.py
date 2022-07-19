import pygame
from model.player import Player
from model.monster import Monster, Alien
from model.comet_event import CometFallEvent
from model.sounds import SoundManager

class Game:

    def __init__(self):
        #generer le joueur en debut
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.pressed = {}
        self.all_monsters = pygame.sprite.Group()
        #definir si le jeu a commence ou non
        self.is_playing = False
        #generer l'evenement des comets
        self.comet_event = CometFallEvent(self)
        self.niveau = 1
        self.difficulty = 0
        self.all_aliens = pygame.sprite.Group()
        self.font = pygame.font.SysFont('Bauhaus 93', 30)
        self.score = 0
        #gerer le son
        self.sound_manager = SoundManager()
        self.compteur = 0
        # self.score_text = ''



    def spawn_alien(self):
        self.all_aliens.add(Alien(self))

    def spawn_monster(self):
        for i in range(10 + self.difficulty ):
            monster = Monster(self)
            self.all_monsters.add(monster)


    def ckeck_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


    def update(self, screen):

        if self.niveau > 5:
            self.niveau = 1

        #afficher le score
        score_text = self.font.render(f'Score : {self.score}', 1, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # appliquer l'image du joueur
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        #actualiser la barre d'evenement
        self.comet_event.update_bar(screen)

        # recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()
        # appliquer l"ensemble des images du groupe projectile
        self.player.all_projectiles.draw(screen)

        # appliquer l'ensemble des images des missiles des monstres
        for monster in self.all_monsters:
            monster.tir_missile()
            monster.all_missiles.draw(screen)
            for missile in monster.all_missiles:
                missile.move()
        # game.monster.all_missiles.draw(screen)

        # appliquer l'ensemble des images des missiles du boss
        for alien in self.all_aliens:
            alien.tir_missile()
            alien.all_missiles.draw(screen)
            for missile in alien.all_missiles:
                missile.move()

        #appliquer les cometes
        self.comet_event.all_comets.draw(screen)
        #recuperer les cometes du jeu
        for comet in self.comet_event.all_comets:
            comet.fall()

        # appliquer les soins
        self.comet_event.all_healths.draw(screen)
        # recuperer les cometes du jeu
        for health in self.comet_event.all_healths:
            health.fall()

        # recuperer les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
        # recuperer les images des monstres
        self.all_monsters.draw(screen)

        # recuperer les aliens du jeu
        for alien in self.all_aliens:
            alien.forward()
            alien.update_health_bar(screen)
        # recuperer les images des monstres
        self.all_aliens.draw(screen)

        # verifier si le joueur souhaite bouger de haut en bas, gauche vers droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x <= 1000:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x >= 0:
            self.player.move_left()
        if self.pressed.get(pygame.K_UP) and self.player.rect.y >= 0:
            self.player.move_up()
        elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y <= 600:
            self.player.move_down()


    def game_over(self):
        #remettre le jeu à neuf
        self.all_monsters = pygame.sprite.Group()
        self.all_aliens = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.player.rect.x = 473
        self.player.rect.y = 500
        self.is_playing = None
        self.comet_event.reset_percent_boss()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.niveau = 1
        # self.score_t()
        print('score', self.score)
        self.get_score()
        # self.score = 0
        self.difficulty = 0
        self.comet_event.all_healths = pygame.sprite.Group()
        #stop la musique
        self.sound_manager.stop('musique')
        #jouer le sons
        self.sound_manager.play('game_over')
        # self.score = 0

    def start(self):
        self.is_playing = True
        self.spawn_monster()
        # self.spawn_alien()
        self.sound_manager.stop('demarrage')
        self.sound_manager.play('musique', 100)
        # if self.is_playing == False:
        self.score = 0

    def add_score(self, amount = 20):
        self.score += amount

    def get_score(self):
        return self.score
