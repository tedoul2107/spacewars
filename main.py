import pygame
from model.game import Game

pygame.init()

#definir une clock
clock = pygame.time.Clock()
FPS = 60

#generer la fenetre du jeu
pygame.display.set_caption('Space Wars')
screen = pygame.display.set_mode((1080, 720))

#mettre le background
background = pygame.image.load('assets/fond1.jpg')

#logo
logo = pygame.image.load('assets/tega.png')
logo = pygame.transform.scale(logo, (613, 357))

#importer la banniere
banner = pygame.image.load('assets/spacewars.png')
banner = pygame.transform.scale(banner, (635, 360))
banner_rect = banner.get_rect()
banner_rect.x = 200
banner_rect.y = 100

#importer le bouton
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = 320
play_button_rect.y = 360

#importer le game_over
game_over = pygame.image.load('assets/game_over.png')
game_over = pygame.transform.scale(game_over, (920, 300))
game_over_rect = game_over.get_rect()
game_over_rect.x = 95
game_over_rect.y = 190


#lire le fichier
fichier = open("assets/score.txt", "r")
bscore = fichier.read()
fichier.close()

nrecord = ''

space_wars = pygame.image.load('assets/spacewars.png')
pygame.display.set_icon(space_wars)

#charger le jeu
game = Game()

#afficher le score
font = pygame.font.SysFont('Bauhaus 93', 50)

running = True

while running:

    #appliquer le background
    if game.compteur < 300:
        # game.compteur += 1
        screen.blit(logo, (180, 200))
    else:
        screen.blit(background, (0, 0))

    #verifier si le jeu a commence ou non
    if game.is_playing:
        game.update(screen)
        nrecord = ''
    elif game.is_playing == False:
        if game.compteur < 300:
            game.compteur += 1
        else:
            screen.blit(play_button, play_button_rect)
            screen.blit(banner, banner_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # si la souris click sur play button
                if play_button_rect.collidepoint(event.pos):
                    # lancer le jeu
                    game.start()
                    # jouer le son
                    game.sound_manager.play("click")
    elif game.is_playing == None:
        screen.blit(game_over, game_over_rect)
        score_text = font.render(f'Score : {game.get_score()}', 1, (255, 255, 255))

        if game.get_score() > int(bscore):
            fichier = open("assets/score.txt", "w+")
            fichier.write(f'{game.get_score()}')
            nrecord = 'New Record'
            bscore = game.get_score()
            fichier.close()

        New_record = font.render(f'{nrecord}', 1, (200, 0, 25))
        screen.blit(New_record, (400, 550))
        best_score_text = font.render(f'Best score : {bscore}', 1, (255, 255, 255))
        screen.blit(score_text, (435, 450))
        screen.blit(best_score_text, (333, 500))


    #mettre à jour l'ecran
    pygame.display.flip()

    #si le joueur ferme la fenetre
    for event in pygame.event.get():
        #verifeir que l'event est la fermeture
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        #detecter si un joueur lache une touche du clavier
        elif event.type == pygame.KEYDOWN:
            #determiner la touche utilisée
            game.pressed[event.key] = True

            #detecter si espace est appuyée pour lancer le projectile
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()

                elif game.is_playing == False:
                    if game.compteur < 300:
                        game.compteur = 300
                    elif game.compteur >= 300:
                        game.start()
                elif game.is_playing == None:
                    game.is_playing = False

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    #fixer le nombre de FPS
    clock.tick(FPS)
